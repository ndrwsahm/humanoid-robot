try:
    print("Ignore the failed commands starting from here if running without ssh")
    from firmware.utility_functions import leg
    from firmware.settings import *
except:
    print("Do not ignore the failed commands past this point if running with ssh")
    from utility_functions import leg
    from settings import *

class Robot:
    def __init__(self, pca_object):
        self.pca_obj = pca_object
        self.new()

    def new(self):
        print('Building Legs...')
        self.left_leg = leg.Leg(self.pca_obj, LEFT_LEG_PINS, "left", (A1_LENGTH, A2_LENGTH, A3_LENGTH))
        self.right_leg = leg.Leg(self.pca_obj, RIGHT_LEG_PINS, "right", (A1_LENGTH, A2_LENGTH, A3_LENGTH))

        #self.left_leg.set_leg_pos(0, 5.36, 6.73)  # starting position
        #self.right_leg.set_leg_pos(0, 5.36, 6.73)  # starting position
        self.left_thetas = self.left_leg.get_leg_thetas()
        self.right_thetas = self.right_leg.get_leg_thetas()
        self.all_thetas = self.left_thetas + self.right_thetas
        self.set_all_angles(self.all_thetas)
    
    def update(self):
        self.left_leg.update()
        self.right_leg.update()

    def set_all_angles(self, angles):
        self.left_leg.set_leg_theta(angles[0], angles[1], angles[2], angles[3], angles[4], angles[5])  # starting 90 degree position
        self.right_leg.set_leg_theta(angles[6], angles[7], angles[8], angles[9], angles[10], angles[11])  # starting 90 degree position
        self.all_thetas = angles

    def get_all_angles(self):
        return self.all_thetas
    
    def set_standing_pos(self):
        pass
     
    def walk_forward(self):
        pass

    def walk_backward(self):
        pass

    def go_to_position(self, x, y):
        pass