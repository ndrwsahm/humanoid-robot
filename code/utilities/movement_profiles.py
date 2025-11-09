import os
import sys

utilities_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, utilities_dir)

from utilities.kinematics import *

STANDING_POS = [-1, 0, -13, -1, 0, -13]

# TODO each function will return nth dim array of angle arrays 
def walk_forward(height, num_steps):
    pass

def walk_backward(height, num_steps):
    pass

def turn_left(height, num_degrees):
    pass

def turn_right(height, num_degrees):
    pass

def strife_left(height, num_steps):
    pass

def strife_right(height, num_steps):
    pass

def stand_still(height):
    all_angles = []
    standing = STANDING_POS

    left_angles = compute_inverse_kinematics(standing[0], standing[1], height, "left")
    right_angles = compute_inverse_kinematics(standing[4], standing[5], height, "right")

    all_angles = [left_angles + right_angles]

    return all_angles