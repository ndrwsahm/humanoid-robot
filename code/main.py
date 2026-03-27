import sys
import threading
sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/')

# Simulated Firmware
from _firmware.instruments import servo_utility
from _firmware.robot import *

# Import GUIs
from GUIs.startup_gui import *
from GUIs.manual_control_gui import *
from GUIs.controller_mode_gui import *

# Import equipment
from equipment.ssh_tx_comms import *
from equipment.ssh_manager import *
from globals import *

# Import utilities
from utilities.kinematics import *
from utilities.movement_profiles import *
from utilities.camera_receiver import CameraReceiver

DEBUG_PRINT_STATEMENT = False
    

class RobotControllerAPI:
    """
    Main application controller.
    Handles:
    - GUI screen switching
    - SSH communication
    - Simulated robot mode
    - Manual control logic (sliders, kinematics, walking)
    - Controller mode
    - Camera streaming
    """
    def __init__(self):

        # Create main Tkinter window
        self.root = tk.Tk()
        self.root.title("Humanoid Robot Controller")

        # -------------------------------
        # INITIAL ROBOT STATE
        # -------------------------------

        # Last known servo angles (12 servos)
        self.last_all_leg_angles = [90] * 12

        # Build standing pose
        self.standing_array = build_stand_still_array(WALKING_HEIGHT)

        # Compute starting foot positions
        left_leg_pos = compute_forward_kinematics(self.standing_array[0], "left")
        right_leg_pos = compute_forward_kinematics(self.standing_array[0], "right")
        starting_leg_pos = left_leg_pos + right_leg_pos

        recal_servos = 0  # Placeholder for future calibration logic

        # -------------------------------
        # GUI SCREENS
        # -------------------------------
        self.screens = {
            "startup": Startup_GUI(GUI_WIDTH, GUI_HEIGHT, HOSTNAME, USERNAME,
                                   FIRMWARE_REMOTE_LOCATION, COM_PORT, BAUDRATE, self.root),

            "manual": Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT,
                                         self.standing_array[0], starting_leg_pos,
                                         recal_servos, self.root),

            "controller": Controller_Mode_GUI(GUI_WIDTH, GUI_HEIGHT, self.root),
        }

        self.current_screen = "startup"
        self.running = True

        # Show startup screen
        self.screens[self.current_screen].pack(fill="both", expand=True)

        # -------------------------------
        # SSH MANAGER SETUP
        # -------------------------------
        self.ssh = SSHManager()
        self.ssh.add_target("pi_robot", HOSTNAME, USERNAME, PASSWORD, FIRMWARE_REMOTE_LOCATION)
        self.ssh.add_target("pi_camera", HOSTNAME_CAMERA, USERNAME_CAMERA,
                            PASSWORD_CAMERA, FIRMWARE_REMOTE_LOCATION_CAMERA)

        # Convenience handles
        self.ssh.tx_robot = self.ssh.targets["pi_robot"]
        self.ssh.tx_camera = self.ssh.targets["pi_camera"]

        # Default SSH target
        self.ssh.select_general("pi_robot")

        # Camera receiver thread
        self.receiver = None

        # Manual control state flag
        self.manual_control_started = False

        # -------------------------------
        # COMMAND DISPATCH TABLE
        # -------------------------------
        self.dispatch = {
            "ssh": lambda: self.run_connect_ssh(),
            "send": lambda: self.ssh.tx_general.send_command(self.screens["startup"].get_command()),
            "firmware": lambda: self.ssh.tx_general.install_firmware(FIRMWARE_LOCAL_LOCATION, self.ssh.tx_general.file_location_on_pi),
            "run_firmware": lambda: self.ssh.tx_general.run_firmware(self.ssh.tx_general.file_location_on_pi),
            "test_accelerometer": lambda: self.run_test_accelerometer(),
            "test_camera": lambda: self.run_test_camera(True),
            "uninstall_firmware": lambda: self.ssh.tx_general.uninstall_firmware(self.ssh.tx_general.file_location_on_pi),
            "raspi_config": lambda: self.ssh.tx_general.run_config(self.ssh.tx_general.file_location_on_pi),
            "reboot": lambda: self.ssh.tx_general.run_reboot(self.ssh.tx_general.file_location_on_pi)
        }

    # ----------------------------------------------------------
    # UNUSED PLACEHOLDERS (future expansion)
    # ----------------------------------------------------------
    def new(self): pass
    def load(self): pass

    # ----------------------------------------------------------
    # EVENT HANDLING (button presses)
    # ----------------------------------------------------------
    def events(self, button):

        # -------------------------------
        # STARTUP SCREEN EVENTS
        # -------------------------------
        if self.current_screen == "startup":

            if button == "manual_control":

                # SIMULATE MODE
                if self.simulate:
                    pca = servo_utility.PCA9865(0x41, True)
                    self.robot = Robot(pca, self.recal_servos)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_manual_control(FIRMWARE_REMOTE_LOCATION,
                                                         self.recal_servos)

                self.manual_control_started = True
                self.switch_screen("manual")

            elif button == "controller_mode":

                # SIMULATE MODE
                if self.simulate:
                    pca = servo_utility.PCA9865(0x41, True)
                    self.robot = Robot(pca, self.recal_servos)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_manual_control(FIRMWARE_REMOTE_LOCATION,
                                                         self.recal_servos)
                    
                self.manual_control_started = True    
                self.switch_screen("controller")

        # -------------------------------
        # MANUAL CONTROL EVENTS
        # -------------------------------
        elif self.current_screen == "manual":

            # Walking forward
            if button == "walk_forward":
                movement = build_walk_array(1, WALKING_HEIGHT, 2, 1)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            # Walking backward
            elif button == "walk_backward":
                movement = build_walk_array(-1, WALKING_HEIGHT, 2, 1)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            # Standing still
            elif button == "stand":
                movement = build_stand_still_array(WALKING_HEIGHT)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            # Exit manual mode
            elif button == "exit":
                self.manual_control_started = False
                self.switch_screen("startup")

        # -------------------------------
        # CONTROLLER MODE EVENTS
        # -------------------------------
        elif self.current_screen == "controller":
            if self.receiver == None:
                    self.run_test_camera(False)

            if button == "walk_forward":
                movement = build_walk_array(1, WALKING_HEIGHT, 2, 1)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "walk_backward":
                movement = build_walk_array(-1, WALKING_HEIGHT, 2, 1)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "stand":
                movement = build_stand_still_array(WALKING_HEIGHT)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "camera":
                    self.receiver.camera_visible = not self.receiver.camera_visible
            
            elif button == "accel":
                self.run_test_accelerometer()
                
            if button == "exit":
                self.switch_screen("startup")

        # -------------------------------
        # DISPATCH COMMANDS
        # -------------------------------
        action = self.dispatch.get(button)
        if action:
            action()

    # ----------------------------------------------------------
    # MAIN UPDATE LOOP (runs every frame)
    # ----------------------------------------------------------
    def screen_update(self):
        screen = self.screens[self.current_screen]

        # -------------------------------
        # STARTUP SCREEN UPDATE
        # -------------------------------
        if self.current_screen == "startup":

            # Read GUI values
            self.simulate = screen.get_simulate_value()
            self.recal_servos = screen.get_recal_value()
            pi_selection = screen.get_pi_selector_value()

            # Update SSH target
            self.ssh.select_general(pi_selection)

            # Update GUI labels
            if pi_selection == "pi_robot":
                screen.update_hostname(self.ssh.tx_robot.hostname)
                screen.update_username(self.ssh.tx_robot.username)
                screen.update_location(self.ssh.tx_robot.file_location_on_pi)
            else:
                screen.update_hostname(self.ssh.tx_camera.hostname)
                screen.update_username(self.ssh.tx_camera.username)
                screen.update_location(self.ssh.tx_camera.file_location_on_pi)

        # -------------------------------
        # MANUAL CONTROL UPDATE LOOP
        # -------------------------------
        elif self.current_screen == "manual":

            screen = self.screens["manual"]

            # 1. Read mode
            mode = screen.get_mode()

            # 2. Compute kinematics
            if mode == "Angles":
                leg_angles = screen.get_all_slider_angles()
                left_pos = compute_forward_kinematics(leg_angles, "left")
                right_pos = compute_forward_kinematics(leg_angles, "right")
                screen.set_all_slider_pos(left_pos + right_pos)

            elif mode == "Kinematics":
                leg_pos = screen.get_all_slider_pos()
                left_angles = compute_inverse_kinematics(leg_pos[0], leg_pos[1], leg_pos[2], "left")
                right_angles = compute_inverse_kinematics(leg_pos[3], leg_pos[4], leg_pos[5], "right")

                # Replace None values with last known angles
                left_angles = self.check_is_none(left_angles, self.last_all_leg_angles, "left")
                right_angles = self.check_is_none(right_angles, self.last_all_leg_angles, "right")

                leg_angles = left_angles + right_angles
                screen.set_all_slider_angles(leg_angles)

            # 3. Send servo commands
            if self.simulate:
                self.robot.set_all_angles(leg_angles)
                self.robot.update()
            else:
                self.last_all_leg_angles = self.send_leg_commands(leg_angles)

        # -------------------------------
        # SSH RESPONSE HANDLING
        # -------------------------------
        if self.ssh.tx_camera.connection:
            response = self.ssh.tx_camera.receive_response()
            if response:
                print(f"Received response: {response}")

        if self.ssh.tx_robot.connection:
            response = self.ssh.tx_robot.receive_response()
            if response:
                print(f"Received response: {response}")

        return screen.gui_update()

    # ----------------------------------------------------------
    # DRAW (optional per-screen drawing)
    # ----------------------------------------------------------
    def draw(self):
        screen = self.screens[self.current_screen]
        if hasattr(screen, "draw"):
            screen.draw()

    # ----------------------------------------------------------
    # MAIN APPLICATION LOOP
    # ----------------------------------------------------------
    def run(self):
        self.new()
        while self.running:
            self.running, button = self.screen_update()
            self.events(button)
            self.draw()

    # ----------------------------------------------------------
    # SCREEN SWITCHING
    # ----------------------------------------------------------
    def switch_screen(self, screen_name):
        self.screens[self.current_screen].pack_forget()
        self.current_screen = screen_name
        self.screens[self.current_screen].pack(fill="both", expand=True)

    # ----------------------------------------------------------
    # SSH CONNECTION HANDLING
    # ----------------------------------------------------------
    def run_connect_ssh(self):
        try:
            self.ssh.tx_robot.connect_ssh()
            self.ssh.tx_camera.connect_ssh()

            self.ssh.tx_robot.connection = True
            self.ssh.tx_camera.connection = True

            if self.ssh.tx_robot.connection and self.ssh.tx_camera.connection:
                print("Successfully connected to both Raspberry Pis via SSH.")
                self.screens["startup"].ssh_connection = True
            else:
                print("Failed to connect to one or both Raspberry Pis via SSH.")
                self.screens["startup"].ssh_connection = False

        except Exception as e:
            print(f"Error occurred while connecting via SSH: {e}")

    # ----------------------------------------------------------
    # CAMERA TESTING
    # ----------------------------------------------------------
    def run_test_camera(self, display_gui):
        if not self.ssh.tx_camera.connection:
            print("Camera Pi not connected!")
            return
        
        print("Starting camera sender...")
        self.ssh.tx_camera.run_test(INSTRUMENTS_REMOTE_LOCATION_CAMERA, CAMERA)
        
        if self.receiver is None:
            print("Starting camera receiver...")
            self.receiver = CameraReceiver(host="0.0.0.0", port=5000)
            self.receiver.camera_visible = display_gui
            threading.Thread(target=self.receiver.receive_data, daemon=True).start()
        else:
            print("Camera receiver already running.")
            print("Toggling camera visibility.")
            self.receiver.camera_visible = display_gui

    # ----------------------------------------------------------
    # ACCELEROMETER TESTING
    # ----------------------------------------------------------
    def run_test_accelerometer(self):
        if self.ssh.tx_robot.connection:
            self.ssh.tx_robot.run_test(INSTRUMENTS_REMOTE_LOCATION, ACCELEROMETER)
        else:
            print("No SSH Connection Established!")

    # ----------------------------------------------------------
    # SERVO COMMAND SENDER
    # ----------------------------------------------------------
    def send_leg_commands(self, all_leg_angles):
        try:
            # Simulation mode
            if self.simulate:
                self.robot.set_all_angles(all_leg_angles)
                self.robot.update()
                return all_leg_angles

            # Real robot mode
            for k in range(NUMBER_OF_SERVOS):
                if self.last_all_leg_angles[k] != all_leg_angles[k]:
                    cmd = f"{ALL_LEG_NAMES[k]}{int(all_leg_angles[k])}\n"
                    #cmd = f"{ALL_LEG_NAMES[k]}{all_leg_angles[k]}\n"
                    self.ssh.tx_robot.send_user_input(cmd)

            response = self.ssh.tx_robot.receive_response()
            if response:
                print(response)

            return all_leg_angles

        except Exception as e:
            print("Sending command error:", e)
            return self.last_all_leg_angles
        
    # ----------------------------------------------------------
    # HANDLE NONE VALUES IN IK
    # ----------------------------------------------------------
    def check_is_none(self, angles, last_angles, leg):
        if angles is None:
            angles = [90] * 6
            for k in range(6):
                if leg == "right":
                    angles[k] = last_angles[k+6]
                else:
                    angles[k] = last_angles[k]
        return angles


# ----------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------
if __name__ == "__main__":
    api = RobotControllerAPI()
    api.run()
