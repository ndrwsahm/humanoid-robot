try:
    from _firmware.firmware_globals import *
except:
    from firmware_globals import *

class Arm:
    def __init__(self, pca_object, side, settings, is_recal):
        self.pca = pca_object

        self.side = side.lower()    # make all lower case                                                  
         
        self.new(settings)
                                                                          
        self.last_thetas = [0, 0, 0]     # shoulder rotator, shoulder aductor, elbow extendor
        self.current_thetas = [90, 90, 90]  # shoulder rotator, shoulder aductor, elbow extendor

        if is_recal:    # Recalibrate servo flag
            self.offset_thetas = [0, 0, 0] 
        else:
            self.offset_thetas = [x - y for x, y in zip(self.default_angles, ANGLES_TO_90)]
  
        self.last_elbow_pos = [0, 0, 0]
        self.last_hand_pos = [0, 0, 0]
        self.current_elbow_pos = [0, 0, 0]
        self.current_hand_pos = [0, 0, 0]

        self.setup()

    def new(self, settings):
        self.pins = (settings["LEFT_ARM_PINS"] if self.side == "left" else settings["RIGHT_ARM_PINS"])
        self.leg_dimensions = (settings["A3_LENGTH"], settings["A4_LENGTH"])
        self.theta_limits = (settings["LEFT_ARM_LIMITS"] if self.side == "left" else settings["RIGHT_ARM_LIMITS"])
        self.default_angles = (settings["LEFT_ARM_DEFAULTS"] if self.side == "left" else settings["RIGHT_ARM_DEFAULTS"])
        self.pulse_width_settings = (settings["LEFT_PULSE_WIDTH_SETTINGS"] if self.side == "left" else settings["RIGHT_PULSE_WIDTH_SETTINGS"])
        self.soft_start_angles = (settings["SOFT_START_ANGLES"])
        #print(self.default_angles)
        
    def setup(self):
        idx = 0
        for pin in self.pins:
            self.pca.set_pulse_min_max(pin, self.pulse_width_settings[idx][PULSE_WIDTH_MIN], self.pulse_width_settings[idx][PULSE_WIDTH_MAX])
            idx += 1

    def update(self):
        self.last_elbow_pos = self.current_elbow_pos
        self.last_hand_pos = self.current_hand_pos

        self.last_thetas = self.current_thetas
    
    def get_pulse_widths(self):
        return self.pulse_width_settings

    def get_arm_pos(self):
        return [self.current_elbow_pos, self.current_hand_pos]
    
    def get_arm_thetas(self):
        return self.current_thetas
    
    def set_arm_pos(self, x, y, z):
        difference = [0, 0, 0, 0, 0, 0] # elbow pos, hand pos

    def set_arm_theta(self, theta1, theta2, theta3):
        
        self.current_thetas = [theta1, theta2, theta3]
        thetas = [theta1, theta2, theta3]
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
