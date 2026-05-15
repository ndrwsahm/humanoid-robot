try:
    from _firmware.firmware_globals import *
    from _firmware.utility_functions.settings_parser import load_robot_settings
    from _firmware.utility_functions.username_id import get_robot_id_from_username
except:
    from firmware_globals import *
    from utility_functions.settings_parser import load_robot_settings
    from utility_functions.username_id import get_robot_id_from_username
class Head:
    def __init__(self, pca_obj, is_recal):
        self.pca_obj = pca_obj

        self.new()

        self.last_thetas = [0, 0]     # roll, yaw
        self.current_thetas = [90, 90]  # roll, yaw

        if is_recal:    # Recalibrate servo flag
            self.offset_thetas = [0, 0] 
        else:
            self.offset_thetas = [x - y for x, y in zip(self.default_angles, [90, 90])]

    def new(self):
        robot_id = get_robot_id_from_username()

        if not robot_id:
            print("Could not determine robot ID from username. Running simulated leg ")
            robot_id = "simulate"

        settings = load_robot_settings(robot_id)

        self.pins = (settings["CAMERA_PINS"][0], settings["CAMERA_PINS"][1])
        self.default_angles = (settings["HEAD_DEFAULTS"][0], settings["HEAD_DEFAULTS"][1])

        #self.pulse_width_settings = settings["CAMERA_PULSE_WIDTH_SETTINGS"]

    def setup(self):
        idx = 0
        for pin in self.pins:
            self.pca_obj.set_pulse_min_max(pin, self.pulse_width_settings[idx][PULSE_WIDTH_MIN], self.pulse_width_settings[idx][PULSE_WIDTH_MAX])
            idx += 1

    def update(self):
        self.last_roll = self.roll
        self.last_yaw = self.yaw

        self.last_thetas = self.current_thetas

    def set_head_theta(self, roll, yaw):
        self.current_thetas = [roll, yaw]   

        if self.current_thetas != self.last_thetas:
            self.pca_obj.set_servo_angle(self.pins[0], yaw + self.offset_thetas[1])  # Example: Set camera angle based on roll
            self.pca_obj.set_servo_angle(self.pins[1], roll + self.offset_thetas[0])  # Example: Set camera angle based on roll


    def get_head_thetas(self):
        return self.current_thetas