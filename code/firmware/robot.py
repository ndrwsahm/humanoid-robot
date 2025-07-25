from firmware.utility_functions import leg
from firmware.settings import *

class Robot:
    def __init__(self, pca):
        self.pca = pca

        self.new()

    def new(self):
        self.left_leg = leg.Leg(self.pca, LEFT_LEG_PINS, "left", (A1_LENGTH, A2_LENGTH, A3_LENGTH))
        self.right_leg = leg.Leg(self.pca, RIGHT_LEG_PINS, "right", (A1_LENGTH, A2_LENGTH, A3_LENGTH))

        #self.left_leg.set_leg_pos(0, 5.36, 6.73)  # starting position
        #self.right_leg.set_leg_pos(0, 5.36, 6.73)  # starting position

    def update(self):
        self.left_leg.update()
        self.right_leg.update()

    def set_all_angles(self, angles):
        self.left_leg.set_leg_theta(angles[0], angles[1], angles[2], angles[3], angles[4], angles[5])  # starting 90 degree position
        self.right_leg.set_leg_theta(angles[6], angles[7], angles[8], angles[9], angles[10], angles[11])  # starting 90 degree position

    def set_standing_pos(self):
        pass
     
    def walk_forward(self):
        pass

    def walk_backward(self):
        pass

    def go_to_position(self, x, y):
        pass