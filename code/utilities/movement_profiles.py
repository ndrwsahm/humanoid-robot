import os
import sys

utilities_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, utilities_dir)

from utilities.kinematics import *

STANDING_POS = [-1, 0, -13, -1, 0, -13]
NUM_FRAMES = 10

def build_swing_phase(direction, center_x, height, step_length, leg):
    
    angles = []

    #print("Swing X Z Pos....")
    if leg == "left":
        y = -3
    else:
        y = 3

    # half circle equation z = sqrt(r^2 - x^2)
    for t in np.linspace(np.pi, 0, NUM_FRAMES):
        x = direction * step_length * np.cos(t) + center_x
        z = 3 * np.sin(t) + height

        #print(x, z)
        angles.append(compute_inverse_kinematics(x, y, z, leg))

    return angles

def build_push_phase(direction, center_x, height, step_length, leg):
    
    angles = []

    #print("Back Step X Z Pos....")
    if leg == "left":
        y = 2
    else:
        y = -2

    #Straight line from end of half circle to back
    for t in np.linspace(1, -1, NUM_FRAMES):
        x = direction * step_length * t + center_x
        z = height

        #print(x, z)
        angles.append(compute_inverse_kinematics(x, y, z, leg))
    
    return angles

# TODO each function will return nth dim array of angle arrays 
def build_walk_array(direction, height, step_length, num_steps):
    for k in range(num_steps):
        swing_phase_left = build_swing_phase(direction, -1, height, step_length, "left")
        swing_phase_right = build_push_phase(direction, -1, height, step_length, "right")
        combined_swing_phases = [swing_phase_left + swing_phase_right for swing_phase_left, swing_phase_right in zip(swing_phase_left, swing_phase_right)]
        
        step_back_phase_left = build_push_phase(direction, -1, height, step_length, "left")
        step_back_phase_right = build_swing_phase(direction, -1, height, step_length, "right")
        combined_step_phase = [step_back_phase_left + step_back_phase_right for step_back_phase_left, step_back_phase_right in zip(step_back_phase_left, step_back_phase_right)]

        movement_array = combined_swing_phases + combined_step_phase

    return movement_array

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

if __name__ == "__main__":
    direction = 1 # forward
    start_x = -1
    height = 12
    step_size = 3

    swing_angles = build_swing_phase(direction, start_x, height, step_size, "left")
    back_step_angles = build_push_phase(direction, start_x, height, step_size, "left")
    print("Swing Angles: ", swing_angles)
    print("")
    print("Back Step Angles: ", back_step_angles)
    print("")
    test_angles = swing_angles + back_step_angles
    print(test_angles)