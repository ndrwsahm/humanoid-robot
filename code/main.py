import sys
import threading
import configparser
import numpy as np
sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/')

# Simulated Firmware
from _firmware.robot import *

# Import GUIs
from GUIs.startup_gui import *
from GUIs.manual_control_gui import *
from GUIs.controller_mode_gui import *
from GUIs.calibrate_servos_gui import Calibrate_Servos_GUI
from GUIs.pwm_calibrate_servos_gui import PWM_Calibrate_Servos_GUI
from GUIs.plan_control_gui import Plan_Control_GUI
from GUIs.utilities.utils import *

# Import equipment
from equipment.ssh_tx_comms import *
from equipment.ssh_manager import *
from globals import *

# Import utilities
from utilities.kinematics import *
from utilities.movement_profiles import *
from utilities.camera_receiver import CameraReceiver
from utilities.write_to_file import *

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
        self.id = ID
        self.new()

        # Last known servo angles (12 servos)
        self.last_all_leg_angles = [90] * 12

        # Build standing pose
        self.standing_array = build_stand_still_array(WALKING_HEIGHT)
        left_leg_angles = self.standing_array[0][:6]   # first 6
        right_leg_angles = self.standing_array[0][6:]  # last 6

        # Compute starting foot positions
        left_leg_pos = compute_forward_kinematics(left_leg_angles, "left")
        right_leg_pos = compute_forward_kinematics(right_leg_angles, "right")
        starting_leg_pos = left_leg_pos + right_leg_pos

        # -------------------------------
        # GUI SCREENS
        # -------------------------------
        self.screens = {
            "startup": Startup_GUI(GUI_WIDTH, GUI_HEIGHT, self.host_name, self.username, self.firmware_remote_location, COM_PORT, BAUDRATE, self.root),

            "manual": Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT,self.standing_array[0], starting_leg_pos, self.root),

            "controller": Controller_Mode_GUI(GUI_WIDTH, GUI_HEIGHT, self.root),

            "calibrate": Calibrate_Servos_GUI(GUI_WIDTH, GUI_HEIGHT, self.root),
            "pwm_calibrate": PWM_Calibrate_Servos_GUI(GUI_WIDTH, GUI_HEIGHT, self.root), # Reusing the same GUI for PWM calibration
            "plan_control": Plan_Control_GUI(GUI_WIDTH, GUI_HEIGHT, self.standing_array[0], starting_leg_pos, self.root)

        }

        self.current_screen = "startup"
        self.running = True
        self.last_steady_cam = False

        # Show startup screen
        self.screens[self.current_screen].pack(fill="both", expand=True)

        # -------------------------------
        # SSH MANAGER SETUP
        # -------------------------------
        self.ssh = SSHManager()
        self.ssh.add_target("pi_robot", self.host_name, self.username, self.password, self.firmware_remote_location)
        self.ssh.add_target("pi_camera", self.host_name_camera, self.username_camera, self.password_camera, self.firmware_remote_location_camera)

        # Convenience handles
        self.ssh.tx_robot = self.ssh.targets["pi_robot"]
        self.ssh.tx_camera = self.ssh.targets["pi_camera"]

        # Default SSH target
        self.ssh.select_general("pi_robot")

        # Camera receiver thread
        self.receiver = None

        # Manual control state flag
        self.manual_control_started = False

        self.imu_buffer = ""
        self.imu_array = []

        # -------------------------------
        # COMMAND DISPATCH TABLE
        # -------------------------------
        self.dispatch = {
            "ssh": lambda: self.run_connect_ssh(),

            "send": lambda: self.safe_ssh(
                self.ssh.tx_general, "send_command",
                self.ssh.tx_general.send_command,
                self.screens["startup"].get_command()
            ),

            "firmware": lambda: self.safe_ssh(
                self.ssh.tx_general, "install_firmware",
                self.ssh.tx_general.install_firmware,
                self.firmware_local_location, self.ssh.tx_general.file_location_on_pi
            ),

            "run_firmware": lambda: self.safe_ssh(
                self.ssh.tx_general, "run_firmware",
                self.ssh.tx_general.run_firmware,
                self.ssh.tx_general.file_location_on_pi
            ),

            "test_accelerometer": lambda: self.safe_ssh(
                self.ssh.tx_robot, "test_accelerometer",
                self.run_test_accelerometer
            ),

            "calibrate_imu": lambda: self.safe_ssh(
                self.ssh.tx_robot, "calibrate_imu",
                self.run_calibrate_imu
            ),

            "test_camera": lambda: self.safe_ssh(
                self.ssh.tx_camera, "test_camera",
                self.run_test_camera, True
            ),

            "uninstall_firmware": lambda: self.safe_ssh(
                self.ssh.tx_general, "uninstall_firmware",
                self.ssh.tx_general.uninstall_firmware,
                self.ssh.tx_general.file_location_on_pi
            ),

            "raspi_config": lambda: self.safe_ssh(
                self.ssh.tx_general, "raspi_config",
                self.ssh.tx_general.run_config,
                self.ssh.tx_general.file_location_on_pi
            ),

            "reboot": lambda: self.safe_ssh(
                self.ssh.tx_general, "reboot",
                self.ssh.tx_general.run_reboot,
                self.ssh.tx_general.file_location_on_pi
            )
        }

    # ----------------------------------------------------------
    # UNUSED PLACEHOLDERS (future expansion)
    # ----------------------------------------------------------
    def new(self): 
        self.main_folder = os.path.dirname(__file__)
        self.utilities_folder = os.path.join(self.main_folder, 'utilities')
        self.custom_profiles_folder = os.path.join(self.utilities_folder, 'custom_profiles')
        self.configuration_folder = os.path.join(self.main_folder, 'configurations')
        self.id_folder = os.path.join(self.configuration_folder, str(self.id))
        self.filename = "configuration.ini"
        self.full_file_path = os.path.join(self.id_folder, self.filename)

        self.config = configparser.ConfigParser()
        self.config.read(self.full_file_path)

        self.getConfigurationVariables()

    def load(self): pass

    def getConfigurationVariables(self):
        self.host_name = self.config.get("HUMANOID_VARS", "HOSTNAME")
        self.host_name_camera = self.config.get("HUMANOID_VARS", "HOSTNAME_CAMERA")
        self.username = self.config.get("HUMANOID_VARS", "USERNAME")
        self.username_camera = self.config.get("HUMANOID_VARS", "USERNAME_CAMERA")
        self.password = self.config.get("HUMANOID_VARS", "PASSWORD")
        self.password_camera = self.config.get("HUMANOID_VARS", "PASSWORD_CAMERA")

        self.firmware_local_location = self.config.get("HUMANOID_VARS", "FIRMWARE_LOCAL_LOCATION")
        self.firmware_remote_location = self.config.get("HUMANOID_VARS", "FIRMWARE_REMOTE_LOCATION")
        self.firmware_remote_location_camera = self.config.get("HUMANOID_VARS", "FIRMWARE_REMOTE_LOCATION_CAMERA")  

        self.instruments_remote_location = self.config.get("HUMANOID_VARS", "INSTRUMENTS_REMOTE_LOCATION")
        self.instruments_remote_location_camera = self.config.get("HUMANOID_VARS", "INSTRUMENTS_REMOTE_LOCATION_CAMERA")

    # ----------------------------------------------------------
    # EVENT HANDLING (button presses)
    # ----------------------------------------------------------
    def events(self, button):
        # -------------------------------
        # STARTUP SCREEN EVENTS
        # -------------------------------
        if self.current_screen == "startup":
            if button == "manual_control":
                if not self.ssh.tx_robot.connection:
                    self.simulate = True
                    print_status(self.screens[self.current_screen], "No SSH Connection Established! Entering SIMULATION MODE.")

                # SIMULATE MODE
                if self.simulate:
                    self.robot = Robot(False)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    #self.recal_servos = self.screens["startup"].get_recal_value()  # Update recalibration setting
                    self.ssh.tx_robot.run_manual_control(self.firmware_remote_location, 0)

                self.manual_control_started = True
                self.switch_screen("manual")

            elif button == "controller_mode":
                if not self.ssh.tx_robot.connection:
                    self.simulate = True
                    print_status(self.screens[self.current_screen], "No SSH Connection Established! Entering SIMULATION MODE.")

                # SIMULATE MODE
                if self.simulate:
                    self.robot = Robot(False)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_manual_control(self.firmware_remote_location, 0)
                    
                self.manual_control_started = True    
                self.switch_screen("controller")

            elif button == "calibrate_servos":
                # SIMULATE MODE
                if self.simulate:
                    self.robot = Robot(False)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_calibrate_servos(self.firmware_remote_location, 0)

                self.manual_control_started = True  
                self.switch_screen("calibrate")

            elif button == "pwm_calibrate_servos":
                # SIMULATE MODE
                if self.simulate:
                    self.robot = Robot(False)

                # REAL ROBOT MODE
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_pwm_calibrate_servos(self.firmware_remote_location, 0)

                self.manual_control_started = True 
                self.switch_screen("pwm_calibrate")

            elif button == "plan_control":
                if self.simulate:
                    self.robot = Robot(False)
                else:
                    self.robot = None
                    self.ssh.tx_robot.run_manual_control(self.firmware_remote_location, 0)
                
                self.manual_control_started = True
                self.switch_screen("plan_control")

        # -------------------------------
        # MANUAL CONTROL EVENTS
        # -------------------------------
        elif self.current_screen == "manual":
            speed = set_speed_val(self, self.screens["manual"].get_speed())
            num_steps = set_num_steps_val(self, self.screens["manual"].get_num_steps())
            step_length = set_step_length_val(self, self.screens["manual"].get_step_length())

            if button == "walk_forward":
                movement = build_walk_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "walk_backward":
                movement = build_walk_array(BACKWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)
            
            elif button == "turn_right":
                movement = build_turn_right_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "turn_left":
                movement = build_turn_left_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
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
            step_length = 2
            num_steps = 1
            speed = 25
            if self.receiver == None:
                    self.run_test_camera(False)

            if button == "walk_forward":
                movement = build_walk_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "walk_backward":
                movement = build_walk_array(BACKWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "turn_right":
                movement = build_turn_right_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
                for step in movement:
                    self.last_all_leg_angles = self.send_leg_commands(step)

            elif button == "turn_left":
                movement = build_turn_left_array(FORWARD, WALKING_HEIGHT, step_length, num_steps, speed)
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
        # Calibrate MODE EVENTS
        # -------------------------------
        elif self.current_screen == "calibrate":
            if button == "calibrate":
                angles = get_all_slider_angles(self.screens["calibrate"])
                print_status(self.screens[self.current_screen], "Saving calibration offsets: {angles}")
                write_cal_data(angles, self.id)
                self.switch_screen("startup")

            elif button == "exit":
                self.switch_screen("startup")

        # -------------------------------
        # Pwm Calibrate MODE EVENTS
        # -------------------------------
        elif self.current_screen == "pwm_calibrate":
            if button == "pwm_calibrate":
                angles = get_all_slider_angles(self.screens["pwm_calibrate"])
                pwm_min_settings, pwm_max_settings = self.screens["pwm_calibrate"].get_pwm_min_max_values()

                pwm_enabled_states = self.screens["pwm_calibrate"].get_pwm_enabled_flags()  # Get the enabled/disabled states of each servo (for future use)
                write_pwm_calibration_data(pwm_min_settings, pwm_max_settings, pwm_enabled_states, self.id)  # Save PWM settings
                self.switch_screen("startup")

        # -------------------------------
        # Plan Control MODE EVENTS
        # -------------------------------
        elif self.current_screen == "plan_control":
            if button == "run_custom_profile":
                filename = self.screens["plan_control"].get_selected_profile_path()
                if filename:
                    full_file_path = os.path.join(self.custom_profiles_folder, filename)
                    angles = load_positions_from_ini(full_file_path)
                    movement = build_custom_profile_from_positions(angles, 30)

                    pos_num = 1
                    for step in movement:
                        pos_num += 1
                        self.last_all_leg_angles = self.send_leg_commands(step)
                else:
                    print_status(self.screens[self.current_screen], "No file selected!!")
                
        # ------
        # -------------------------
        # DISPATCH COMMANDS
        # -------------------------------
        if button != "none":
            print_status(self.screens[self.current_screen], f"Running {button}...")
        action = self.dispatch.get(button)
        if action:
            print_statements = action()
            if print_statements:
                for msg in print_statements:
                    print_status(self.screens[self.current_screen], msg)

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

        else:
            screen = self.screens[self.current_screen]

            if self.current_screen == "manual":
                steady_cam_gui_var = self.screens[self.current_screen].get_steady_camera()
                if self.last_steady_cam != steady_cam_gui_var:
                    if steady_cam_gui_var:
                        #self.send_head_commands([70,70])
                        self.send_special_command("scy\n")
                    else:
                        self.send_special_command("scn\n")
                self.last_steady_cam = steady_cam_gui_var
            # 1. Read mode
            mode = screen.get_mode()

            # 2. Compute kinematics
            if mode == "Angles":
                leg_angles = get_all_slider_angles(screen)
                left_leg_angles  = leg_angles[0:6]
                right_leg_angles = leg_angles[6:12]

                #arm_angles = get_all_slider_arm_angles(screen)
                #left_arm_angles = arm_angles[0:3]
                #right_arm_angles = arm_angles[3:6]
                head_angles = get_all_slider_head_angles(screen)
 
                left_pos  = compute_forward_kinematics(left_leg_angles, "left")
                right_pos = compute_forward_kinematics(right_leg_angles, "right")

                set_all_slider_pos(screen, left_pos + right_pos)

            elif mode == "Kinematics":
                leg_pos = get_all_slider_pos(screen)
           
                left_angles = compute_inverse_kinematics(leg_pos[0], leg_pos[1], leg_pos[2], "left")
                right_angles = compute_inverse_kinematics(leg_pos[3], leg_pos[4], leg_pos[5], "right")

                # Replace None values with last known angles
                left_angles = self.check_is_none(left_angles, self.last_all_leg_angles, "left")
                right_angles = self.check_is_none(right_angles, self.last_all_leg_angles, "right")

                leg_angles = left_angles + right_angles
                set_all_slider_angles(screen, leg_angles)

            # 3. Send servo commands
            if self.simulate:
                self.robot.set_all_angles(leg_angles)
                self.robot.update()
            else:
                self.last_all_leg_angles = self.send_leg_commands(leg_angles)
                self.last_all_head_angles = self.send_head_commands(head_angles)
       
        # -------------------------------
        # SSH RESPONSE HANDLING
        # -------------------------------
        if self.ssh.tx_camera.connection:
            response = self.ssh.tx_camera.receive_response()
            if response:
                print_status(self.screens[self.current_screen], f"Received response from Camera: {response}")

        if self.ssh.tx_robot.connection:
            response = self.ssh.tx_robot.receive_response()
            if response:
                if self.get_imu_data_readback(self.screens[self.current_screen], response):
                    pass
                else:
                    print_status(self.screens[self.current_screen], f"Received response from Camera: {response}")
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
    def safe_ssh(self, target, action_name, func, *args, **kwargs):
        """
        Safely executes an SSH action.
        Returns a list of print statements collected by the SSH object.
        """
        # Not connected
        if not target.connection:
            msg = f"[SSH ERROR] Cannot run '{action_name}': {target.hostname} is not connected."
            print_status(self.screens[self.current_screen], msg)
            target.print_statements.append(msg)

            # return + clear
            result = list(target.print_statements)
            target.print_statements.clear()
            return result

        try:
            # Run the SSH action
            func(*args, **kwargs)

        except Exception as e:
            msg = f"[SSH ERROR] '{action_name}' failed: {e}"
            print_status(self.screens[self.current_screen], msg)
            target.print_statements.append(msg)

        # ALWAYS return the collected print statements
        result = list(target.print_statements)
        target.print_statements.clear()
        return result

    def run_connect_ssh(self):
        try:
            self.ssh.tx_robot.connect_ssh()
            self.ssh.tx_camera.connect_ssh()

            if self.ssh.tx_robot.connection:
                print_status(self.screens[self.current_screen], "Successfully connected to servo control Raspberry Pi via SSH.")
                self.screens["startup"].robot_servo_connection = True
            else:
                print_status(self.screens[self.current_screen], "Failed to connect to servo control Raspberry Pi via SSH.")
                self.screens["startup"].robot_servo_connection = False

            if self.ssh.tx_camera.connection:
                print_status(self.screens[self.current_screen], "Successfully connected to camera Raspberry Pi via SSH.")
                self.screens["startup"].robot_camera_connection = True
            else:
                print_status(self.screens[self.current_screen], "Failed to connect to camera Raspberry Pi via SSH.")
                self.screens["startup"].robot_camera_connection = False

        except Exception as e:
            print_status(self.screens[self.current_screen], f"Error occurred while connecting via SSH: {e}")

    # ----------------------------------------------------------
    # CAMERA TESTING
    # ----------------------------------------------------------
    def run_test_camera(self, display_gui):
        if not self.ssh.tx_camera.connection:
            print_status(self.screens[self.current_screen], "Camera Pi not connected!")
            return
        
        print_status(self.screens[self.current_screen], "Starting camera sender...")
        self.ssh.tx_camera.run_test(self.instruments_remote_location_camera, CAMERA)
        
        if self.receiver is None:
            print_status(self.screens[self.current_screen],"Starting camera receiver...")
            self.receiver = CameraReceiver(host="0.0.0.0", port=5000)
            self.receiver.camera_visible = display_gui
            threading.Thread(target=self.receiver.receive_data, daemon=True).start()
        else:
            print_status(self.screens[self.current_screen], "Camera receiver already running.")
            print_status(self.screens[self.current_screen], "Toggling camera visibility.")
            self.receiver.camera_visible = display_gui

    # ----------------------------------------------------------
    # ACCELEROMETER TESTING
    # ----------------------------------------------------------
    def run_test_accelerometer(self):
        if self.ssh.tx_robot.connection:
            threading.Thread(target=self.ssh.tx_robot.run_test, args=(self.instruments_remote_location, ACCELEROMETER)).start()
            #self.ssh.tx_robot.run_test(self.instruments_remote_location, ACCELEROMETER)
        else:
            print_status(self.screens[self.current_screen], "No SSH Connection Established!")

    def run_calibrate_imu(self):
        # Clear old IMU data
        self.imu_array = []
        self.imu_buffer = ""

        # Start accelerometer test
        self.ssh.tx_robot.run_test(self.instruments_remote_location, ACCELEROMETER)

        # Schedule stop after 3 seconds
        self.root.after(3000, self.finish_calibration)

    def finish_calibration(self):
        # Stop the remote IMU script
        self.ssh.tx_robot.send_command("pkill -f accelerometer.py")

        # Compute average IMU values
        if len(self.imu_array) == 0:
            print_status(self.screens[self.current_screen], "No IMU data collected!")
            return

        # Average each column
        imu_np = np.array(self.imu_array)
        avg = np.mean(imu_np, axis=0)
        avg = np.round(avg, 2)
        print_status(self.screens[self.current_screen], f"IMU AVERAGE: {avg}")

        # TODO: compute real calibration angles from avg
        angles = [avg[0], avg[1], avg[2]]

        write_imu_data(angles, self.id)

        print_status(self.screens[self.current_screen], "Calibrate IMU Complete!")
        print_status(self.screens[self.current_screen], "Be sure to click Install Firmware to apply changes!!!")

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

            self.print_response(self.screens[self.current_screen])

            return all_leg_angles

        except Exception as e:
            print("Sending command error:", e)
            return self.last_all_leg_angles

    def send_head_commands(self, head_angles):
        try:
            # Simulation mode
            if self.simulate:
                self.robot.head.set_head_angles(head_angles)
                self.robot.update()
                return head_angles

            # Real robot mode
            for k in range(len(head_angles)):
                if self.last_all_head_angles[k] != head_angles[k]:
                    cmd = f"{ALL_HEAD_NAMES[k]}{int(head_angles[k])}\n"
                    self.ssh.tx_robot.send_user_input(cmd)

            self.print_response(self.screens[self.current_screen])

            return head_angles

        except Exception as e:
            print_status(self.screens[self.current_screen], f"Sending head command error: {e}")
            return head_angles
        
    def send_special_command(self, cmd):
        try:
            if self.simulate:
                pass
            
            self.ssh.tx_robot.send_user_input(cmd)

            self.print_response(self.screens[self.current_screen])

        except Exception as e:
            print_status(self.screens[self.current_screen], f"Sending head command error: {e}")
        
    def send_pwm_leg_commands(self, all_pwm_settings, all_leg_angles):
        try:
            # Simulation mode
            if self.simulate:
                self.robot.set_all_angles(all_leg_angles)
                self.robot.update()
                return all_leg_angles

            # Real robot mode
            for k in range(NUMBER_OF_SERVOS):
                if self.last_all_leg_angles[k] != all_leg_angles[k]:
                    cmd = f"pwm{ALL_LEG_NAMES[k]}x{all_pwm_settings[k][0]}x{all_pwm_settings[k][1]}x{int(all_leg_angles[k])}\n"
                    #cmd = f"{ALL_LEG_NAMES[k]}{all_leg_angles[k]}\n"
                    self.ssh.tx_robot.send_user_input(cmd)

            self.print_response(self.screens[self.current_screen])

            return all_leg_angles

        except Exception as e:
            print_status(self.screens[self.current_screen], f"Sending head command error: {e}")
            return self.last_all_leg_angles
        
    # Print Entry Point
    ####################################
    def print_response(self, current_screen):
        if self.ssh.tx_robot.connection:
                response = self.ssh.tx_robot.receive_response()
                if response:
                    if self.get_imu_data_readback(current_screen, response):
                        pass
                    else:
                        print_status(current_screen, response)

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

    def get_imu_data_readback(self, current_screen, response):
        if response[:3] == "IMU":
            try:
                self.imu_values = self.handle_imu_stream(current_screen, response)
                self.imu_array.append(self.imu_values)
                print_status(current_screen, f"{self.imu_values}")
            except Exception as e:
                print_status(current_screen, f"Error in parsing: {e}")

            return True
        else:
            return False
    def handle_imu_stream(self, current_screen, response):
        # Append new data to buffer
        self.imu_buffer += response

        # Split into lines
        lines = self.imu_buffer.split("\n")

        # Keep the last partial line in the buffer
        self.imu_buffer = lines[-1]

        # Process all complete lines
        for line in lines[:-1]:
            clean = line.strip()

            if clean.startswith("IMU:"):
                try:
                    # Remove prefix
                    clean = clean.replace("IMU:", "").strip()
                    parts = [p.strip() for p in clean.split(",")]
                    values = [float(p) for p in parts]

                    return values

                except Exception as e:
                    print_status(current_screen, f"Error in parsing: {e}")

# ----------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------
if __name__ == "__main__":
    api = RobotControllerAPI()
    api.run()
