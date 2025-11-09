import os
import sys

utilities_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, utilities_dir)

from utilities.kinematics import *

STANDING_POS = [-1, 0, -13, -1, 0, -13]

# TODO each function will return nth dim array of angle arrays 
def build_walk_forward_array(height, num_steps):
    pass

def build_walk_backward_array(height, num_steps):
    pass

def build_turn_left_array(height, num_degrees):
    pass

def build_turn_right_array(height, num_degrees):
    pass

def build_strife_left_array(height, num_steps):
    pass

def build_strife_right_array(height, num_steps):
    pass

def build_stand_still_array(height):
    all_angles = []
    standing = STANDING_POS

    left_angles = compute_inverse_kinematics(standing[0], standing[1], height, "left")
    right_angles = compute_inverse_kinematics(standing[3], standing[4], height, "right")

    all_angles = [left_angles + right_angles]

    return all_angles