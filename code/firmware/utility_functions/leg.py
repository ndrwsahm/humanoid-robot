import math
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
    def __init__(self, pca_object, pin_numbers, side, dimensions):
        self.pca = pca_object
        self.pins = pin_numbers
        self.side = side.lower()    # make all lower case                                                  
                                                                           
        self.leg_dimensions = dimensions    # {a1, a2, a3}    

        self.last_thetas = [0, 0, 0, 0, 0, 0]     # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
        self.current_thetas = [90, 90, 90, 90, 90, 90]  # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

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

    def compute_inverse_kinematics(self, x, y, z):
        theta = [0, 0, 0, 0, 0, 0]

        return theta
    
    def compute_forward_kinematics(self, theta1, theta2, theta3):
        x = 0
        y = 0
        z = 0

        return [x, y, z]

    def check_work_envelope(self, x, y, z):
        return True
    
    def get_leg_pos(self):
        return [self.current_knee_pos, self.current_foot_pos]
    
    def get_leg_thetas(self):
        return self.current_thetas
    
    def set_leg_pos(self, x, y, z):
        difference = [0, 0, 0, 0, 0, 0] # knee pos, foot pos

    def set_leg_theta(self, theta1, theta2, theta3, theta4, theta5, theta6):
        
        self.current_thetas = [theta1, theta2, theta3, theta4, theta5, theta6]
        print(self.current_thetas, self.pins)
        if self.last_thetas != self.current_thetas:
            self.pca.set_servo_angle(self.pins[0], theta1)
            self.pca.set_servo_angle(self.pins[1], theta2)
            self.pca.set_servo_angle(self.pins[2], theta3)
            self.pca.set_servo_angle(self.pins[3], theta4)
            self.pca.set_servo_angle(self.pins[4], theta5)
            self.pca.set_servo_angle(self.pins[5], theta6)
