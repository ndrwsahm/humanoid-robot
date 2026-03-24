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
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Humanoid Robot Controller")

        # Create Soft Start Angles
        self.last_all_leg_angles = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
        self.standing_array = build_stand_still_array(WALKING_HEIGHT)
        left_leg_pos = compute_forward_kinematics(self.standing_array[0], "left")
        right_leg_pos = compute_forward_kinematics(self.standing_array[0], "right")
        starting_leg_pos = left_leg_pos + right_leg_pos
        recal_servos = 0    # TODO need to figure out how to cal servos

        # Initialize GUIs
        self.screens = {
            "startup": Startup_GUI(GUI_WIDTH, GUI_HEIGHT, HOSTNAME, USERNAME, FIRMWARE_REMOTE_LOCATION, COM_PORT, BAUDRATE, self.root),
            "manual": Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT, self.standing_array[0], starting_leg_pos, recal_servos, self.root),
            "controller": Controller_Mode_GUI(GUI_WIDTH, GUI_HEIGHT, self.root),
        }

        self.current_screen = "startup"
        self.running = True

        self.screens[self.current_screen].pack(fill="both", expand=True)
        
        # Create SSH Manager and add targets
        self.ssh = SSHManager()
        self.ssh.add_target("pi_robot", HOSTNAME, USERNAME, PASSWORD, FIRMWARE_REMOTE_LOCATION)
        self.ssh.add_target("pi_camera", HOSTNAME_CAMERA, USERNAME_CAMERA, PASSWORD_CAMERA, FIRMWARE_REMOTE_LOCATION_CAMERA)

        self.ssh.tx_robot = self.ssh.targets["pi_robot"]
        self.ssh.tx_camera = self.ssh.targets["pi_camera"]
        self.ssh.select_general("pi_robot")   # default

        # Camera receiver
        self.receiver = None

        # Command dispatch dictionary
        self.dispatch = {
        "ssh": lambda: self.run_connect_ssh(),
        #"nrf": lambda: run_connect_nrf(),
        #"send": lambda: ssh.tx_general.send_command(start_gui.get_command()),
        "firmware": lambda: self.ssh.tx_general.install_firmware(FIRMWARE_LOCAL_LOCATION, self.ssh.tx_general.file_location_on_pi),
        #"run_firmware": lambda: run_firmware(ssh.tx_general),
        "test_accelerometer": lambda: self.run_test_accelerometer(),
        "test_camera": lambda: self.run_test_camera(True),
        #"uninstall_firmware": lambda: ssh.tx_general.uninstall_firmware(ssh.tx_general.file_location_on_pi),
        "raspi_config": lambda: self.ssh.tx_general.run_config(self.ssh.tx_general.file_location_on_pi),
        #"reboot": lambda: ssh.tx_general.run_reboot(ssh.tx_general.file_location_on_pi)
        }

    def new(self):
        pass
    
    def load(self):
        pass

    def events(self, button):
        if self.current_screen == "startup":
            if button == "manual_control":
                self.switch_screen("manual")
            elif button == "controller_mode":
                self.switch_screen("controller")

        elif self.current_screen == "manual":
            if button == "exit":
                self.switch_screen("startup")

        elif self.current_screen == "controller":
            if button == "exit":
                self.switch_screen("startup")

        action = self.dispatch.get(button)
        if action:
            action()

    def screen_update(self):
        screen = self.screens[self.current_screen]

        if self.current_screen == "startup":
            self.simulate = screen.get_simulate_value()
            self.recal_servos = screen.get_recal_value()
            pi_selection = screen.get_pi_selector_value()

            # Update SSH target selection
            self.ssh.select_general(pi_selection)

            # Update labels dynamically
            if pi_selection == "pi_robot":
                screen.update_hostname(self.ssh.tx_robot.hostname)
                screen.update_username(self.ssh.tx_robot.username)
                screen.update_location(self.ssh.tx_robot.file_location_on_pi)
            else:
                screen.update_hostname(self.ssh.tx_camera.hostname)
                screen.update_username(self.ssh.tx_camera.username)
                screen.update_location(self.ssh.tx_camera.file_location_on_pi)

        elif self.current_screen == "manual":
            if self.simulate:
                # Intialize simulated robot from firmware folder
                pca = servo_utility.PCA9685(0x41, self.simulate)
                robot = Robot(pca, self.recal_servos)
            else:
                robot = None
                self.ssh.tx_robot.run_manual_control(FIRMWARE_REMOTE_LOCATION, self.rf_connection, self.recal_servos)

        if self.ssh.tx_camera.connection:
            response = self.ssh.tx_camera.receive_response()
            if response:
                print(f"Received response: {response}")

        if self.ssh.tx_robot.connection:
            response = self.ssh.tx_robot.receive_response()
            if response:
                print(f"Received response: {response}")

        return screen.gui_update()
    
    def draw(self):
        screen = self.screens[self.current_screen]
        if hasattr(screen, "draw"):
            screen.draw()

    def run(self):
        self.new()
        while self.running:
            self.running, button = self.screen_update()
            self.events(button)
            self.draw()

    def switch_screen(self, screen_name):
        # Hide current screen
        self.screens[self.current_screen].pack_forget()

        # Show new screen
        self.current_screen = screen_name
        self.screens[self.current_screen].pack(fill="both", expand=True)

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

    def run_test_camera(self, display_gui):
        if not self.ssh.tx_camera.connection:
            print("Camera Pi not connected!")
            return
        
        print("Starting camera sender...")
        self.ssh.tx_camera.send_command(f"python3 {INSTRUMENTS_REMOTE_LOCATION_CAMERA}/{CAMERA}.py &")

        print("Starting camera receiver...")
        if self.receiver is None:
            self.receiver = CameraReceiver(host="0.0.0.0", port=5000)
            self.receiver.camera_visible = display_gui
            threading.Thread(target=self.receiver.receive_data, daemon=True).start()
        else:
            self.receiver.camera_visible = display_gui

    def run_test_accelerometer(self):
        if(self.ssh.tx_robot.connection):
            self.ssh.tx_robot.run_test(INSTRUMENTS_REMOTE_LOCATION, ACCELEROMETER)

        else:
            print("No SSH Connection Established!")

if __name__ == "__main__":
    api = RobotControllerAPI()
    api.run()