try:
    from _firmware.firmware_globals import *
    from _firmware.utility_functions.settings_parser import load_robot_settings
    from _firmware.utility_functions.username_id import get_robot_id_from_username
except:
    from firmware_globals import *
    from utility_functions.settings_parser import load_robot_settings
    from utility_functions.username_id import get_robot_id_from_username

class Leg:
    def __init__(self, pca_object, side, is_recal):
        self.pca = pca_object

        self.side = side.lower()    # make all lower case                                                  
         
        self.new()
                                                                          
        self.last_thetas = [0, 0, 0, 0, 0, 0]     # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
        self.current_thetas = [90, 90, 90, 90, 90, 90]  # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

        if is_recal:    # Recalibrate servo flag
            self.offset_thetas = [0, 0, 0, 0, 0, 0] 
        else:
            self.offset_thetas = [x - y for x, y in zip(self.default_angles, ANGLES_TO_90)]
  
        self.last_knee_pos = [0, 0, 0]
        self.last_foot_pos = [0, 0, 0]
        self.current_knee_pos = [0, 0, 0]
        self.current_foot_pos = [0, 0, 0]

        self.setup()

    def new(self):
        robot_id = get_robot_id_from_username()

        if not robot_id:
            print("Could not determine robot ID from username. Running simulated leg ")
            robot_id = "simulate"

        settings = load_robot_settings(robot_id)

        self.pins = (settings["LEFT_LEG_PINS"] if self.side == "left" else settings["RIGHT_LEG_PINS"])
        self.leg_dimensions = (settings["A1_LENGTH"], settings["A2_LENGTH"])
        self.theta_limits = (settings["LEFT_LIMITS"] if self.side == "left" else settings["RIGHT_LIMITS"])
        self.default_angles = (settings["LEFT_DEFAULTS"] if self.side == "left" else settings["RIGHT_DEFAULTS"])
        self.pulse_width_settings = (settings["LEFT_PULSE_WIDTH_SETTINGS"] if self.side == "left" else settings["RIGHT_PULSE_WIDTH_SETTINGS"])
        self.soft_start_angles = (settings["SOFT_START_ANGLES"])
        #print(self.default_angles)
        
    def setup(self):
        idx = 0
        for pin in self.pins:
            self.pca.set_pulse_min_max(pin, self.pulse_width_settings[idx][PULSE_WIDTH_MIN], self.pulse_width_settings[idx][PULSE_WIDTH_MAX])
            idx += 1

    def update(self):
        self.last_knee_pos = self.current_knee_pos
        self.last_foot_pos = self.current_foot_pos

        self.last_thetas = self.current_thetas
    
    def get_pulse_widths(self):
        return self.pulse_width_settings

    def get_leg_pos(self):
        return [self.current_knee_pos, self.current_foot_pos]
    
    def get_leg_thetas(self):
        return self.current_thetas
    
    def set_leg_pos(self, x, y, z):
        difference = [0, 0, 0, 0, 0, 0] # knee pos, foot pos

    def set_leg_theta(self, theta1, theta2, theta3, theta4, theta5, theta6):
        
        self.current_thetas = [theta1, theta2, theta3, theta4, theta5, theta6]
        thetas = [theta1, theta2, theta3, theta4, theta5, theta6]
        #print ("Current thetas")
        #print(self.current_thetas, self.pins)
        #print ("")

        if self.last_thetas != self.current_thetas:
            for k in range(len(self.current_thetas)):
                try:
                    self.pca.set_servo_angle(self.pins[k], thetas[k] + self.offset_thetas[k])
                except Exception as e:
                    print(e)
                    print("Tried to set angle to :", thetas[k]+ self.offset_thetas[k])
                    print("Last theta", self.last_thetas[k])
                    # TODO errors out here and ankle angles get weird
                    self.pca.set_servo_angle(self.pins[k], self.last_thetas[k])

            self.update()

    def set_servo_pwm_settings(self, servo, pwm_min, pwm_max):
        self.pca.set_pulse_min_max(self.pins[servo], pwm_min, pwm_max)
