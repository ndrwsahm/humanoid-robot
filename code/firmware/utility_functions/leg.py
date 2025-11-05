try:
    from firmware.settings import *
except:
    from settings import *

DEBUG_PRINT_IK = False
DEBUG_PRINT_FK = False
DEBUG_PRINT_POS = False

HIP_ROTATOR = 0
HIP_ADUCTOR = 1
HIP_EXTENDOR = 2
KNEE = 3
ANKLE_ADUCTOR = 4
ANKLE_EXTENDOR = 5

class Leg:
    def __init__(self, pca_object, pin_numbers, side, dimensions, limits, is_recal):
        self.pca = pca_object
        self.pins = pin_numbers
        self.side = side.lower()    # make all lower case                                                  
                                                                           
        self.leg_dimensions = dimensions    # {a1, a2}    
        self.theta_limits = limits

        self.last_thetas = [0, 0, 0, 0, 0, 0]     # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
        self.current_thetas = [90, 90, 90, 90, 90, 90]  # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

        if is_recal:    # Recalibrate servo flag
            self.offset_thetas = [0, 0, 0, 0, 0, 0] 
        else:
            if side == "left":
                self.offset_thetas = LEFT_OFFSET_ANGLES
            else:
                self.offset_thetas = RIGHT_OFFSET_ANGLES

        self.last_knee_pos = [0, 0, 0]
        self.last_foot_pos = [0, 0, 0]
        self.current_knee_pos = [0, 0, 0]
        self.current_foot_pos = [0, 0, 0]
        
        self.setup()

    def setup(self):
        for pin in self.pins:
            self.pca.set_pulse_min_max(pin, PULSE_WIDTH_SETTINGS[pin][PULSE_WIDTH_MIN], PULSE_WIDTH_SETTINGS[pin][PULSE_WIDTH_MAX])

    def update(self):
        self.last_knee_pos = self.current_knee_pos
        self.last_foot_pos = self.current_foot_pos

        self.last_thetas = self.current_thetas

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
                    self.pca.set_servo_angle(self.pins[k], self.last_thetas[k])
            #self.pca.set_servo_angle(self.pins[1], theta2 + self.offset_thetas[1])
            #self.pca.set_servo_angle(self.pins[2], theta3 + self.offset_thetas[2])
            #self.pca.set_servo_angle(self.pins[3], theta4 + self.offset_thetas[3])
            #self.pca.set_servo_angle(self.pins[4], theta5 + self.offset_thetas[4])
            #self.pca.set_servo_angle(self.pins[5], theta6 + self.offset_thetas[5])

            self.update()
