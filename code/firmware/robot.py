try:
    print("Ignore the failed commands starting from here if running without ssh")
    from firmware.utility_functions import leg
    from firmware.settings import *
except:
    print("Do not ignore the failed commands past this point if running with ssh")
    from utility_functions import leg
    from settings import *

import time

class Robot:
    def __init__(self, pca_object, is_recal):
        self.pca_obj = pca_object
        self.is_recal = is_recal    # Recalibrate servo flag
        self.new()

    def new(self):
        print('Building Legs...')
        self.left_leg = leg.Leg(self.pca_obj, LEFT_LEG_PINS, "left", (A1_LENGTH, A2_LENGTH), LEFT_LEG_ANGLE_LIMITS, self.is_recal)
        self.right_leg = leg.Leg(self.pca_obj, RIGHT_LEG_PINS, "right", (A1_LENGTH, A2_LENGTH), RIGHT_LEG_ANGLE_LIMITS, self.is_recal)

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
        angles = STANDING_ANGLES
        self.set_all_angles(angles)

    def lean_right(self):
        last_angles = self.get_all_angles()
        end_angles = RIGHT_LEAN_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)
        
    def lean_left(self):
        last_angles = self.get_all_angles()
        end_angles = LEFT_LEAN_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)

    def stand_right_leg(self):
        last_angles = self.get_all_angles()
        end_angles = RIGHT_LEG_STAND_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)

    def stand_left_leg(self):
        last_angles = self.get_all_angles()
        end_angles = LEFT_LEG_STAND_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)

    def swing_left_leg(self):
        last_angles = self.get_all_angles()
        end_angles = LEFT_LEG_FORWARD_STEP_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)

    def swing_right_leg(self):
        last_angles = self.get_all_angles()
        end_angles = RIGHT_LEG_FORWARD_STEP_ANGLES.copy()
        self.smooth_transition_position(last_angles, end_angles)
             
    def walk_forward(self):
        pass

    def walk_backward(self):
        pass

    def smooth_transition_position(self, last_angles, end_angles):
        new_angles = last_angles
        final_true_angles = end_angles.copy()
        fail_list = [1,1,1,1,1,1,1,1,1,1,1,1]

        X = 0.75

        for k in range(len(end_angles)):
            end_angles[k] *= (1-X)

        running = True
        while running:
            for j in range(len(last_angles)):
                last_angles[j] *= X

                new_angles[j] = end_angles[j] + last_angles[j]
                new_angles_rounded = [round(num, 2) for num in new_angles]

                # If difference is less than 1 degree
                if abs(final_true_angles[j] - new_angles[j]) < 1:
                    fail_list[j] = 0
                #print("End Angle" + str(final_true_angles[j]) + " -  New Angle " + str(new_angles[j]) + " = " + str(final_true_angles[j] - new_angles[j]))
            #print("Fail List:   " + str(fail_list))
            if all(item == 0 for item in fail_list):
                running = False
                
            #print("New Angles:    " + str(new_angles_rounded))
            self.set_all_angles(new_angles_rounded)
            last_angles = new_angles_rounded

            time.sleep(0.05) 