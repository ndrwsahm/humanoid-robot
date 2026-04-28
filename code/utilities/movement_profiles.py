import os
import sys

from globals import *

utilities_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, utilities_dir)
print("Utilities directory added to path: ", utilities_dir)
from utilities.kinematics import *

STANDING_POS = [FOOT_X_CENTER, 0, WALKING_HEIGHT, FOOT_X_CENTER, 0, WALKING_HEIGHT]

def convert_speed_to_frames(speed):
    min_frames = 5
    max_frames = 60
    return int(max_frames - (speed / 100) * (max_frames - min_frames))

def build_swing_phase(direction, center_x, height, step_length, speed, leg):
    
    angles = []
    step_height = 2.0

    if leg == "left":
        y = -FOOT_Y_SWING
        print("Left Leg Swing")
    else:
       y = FOOT_Y_SWING
       print("Right Leg Swing")

    # half circle equation z = sqrt(r^2 - x^2)
    print("Swing Step X Z Pos....")
    for t in np.linspace(np.pi, 0, convert_speed_to_frames(speed)):
        x = direction * step_length * np.cos(t) + center_x
        z = step_height * np.sin(t) + height

        print(x, z)
        angles.append(compute_inverse_kinematics(x, y, z, leg))

    return angles

def build_push_phase(direction, center_x, height, step_length, speed, leg):
    
    angles = []

    
    if leg == "left":
        y = FOOT_Y_PUSH
        print("Left Leg Push")
    else:
        y = -FOOT_Y_PUSH
        print("Right Leg Push")

    print("Back Step X Z Pos....")
    #Straight line from end of half circle to back
    for t in np.linspace(step_length, -step_length, convert_speed_to_frames(speed)):
        x = direction * t + center_x
        z = height

        print(x, z)
        angles.append(compute_inverse_kinematics(x, y, z, leg))
    
    return angles

def build_lean_phase(direction, center_x, height, speed, leg):
    
    angles = []
    if direction == LEFT and leg == "left":
        y_start = 0
        y_end = -FOOT_Y_SWING
    elif direction == LEFT and leg == "right":
        y_start = 0
        y_end = -FOOT_Y_PUSH

    elif direction == TRANSITION and leg == "left":
        y_start = -FOOT_Y_SWING
        y_end = FOOT_Y_PUSH
    elif direction == TRANSITION and leg == "right":    
        y_start = -FOOT_Y_PUSH
        y_end = FOOT_Y_SWING

    elif direction == RIGHT and leg == "left":
        y_start = FOOT_Y_PUSH
        y_end = 0
    else:
        y_start = FOOT_Y_SWING
        y_end = 0  

    for t in np.linspace(y_start, y_end, convert_speed_to_frames(speed)):
        y = t
        z = height

        #print(x, z)
        angles.append(compute_inverse_kinematics(center_x, y, z, leg))

    return angles

# TODO each function will return nth dim array of angle arrays 
def build_walk_array(direction, height, step_length, num_steps, speed):
    lean_left_left = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "left")
    lean_left_right = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_left = [lean_left_left + lean_left_right for lean_left_left, lean_left_right in zip(lean_left_left, lean_left_right)]
    
    swing_phase_left = build_swing_phase(direction, FOOT_X_CENTER, height+1, step_length, speed, "left")
    swing_phase_right = build_push_phase(direction, FOOT_X_CENTER, height, step_length, speed, "right")
    combined_swing_phases = [swing_phase_left + swing_phase_right for swing_phase_left, swing_phase_right in zip(swing_phase_left, swing_phase_right)]
    
    transition_phase_left = build_lean_phase(TRANSITION, FOOT_X_CENTER, height, speed, "left")
    transition_phase_right = build_lean_phase(TRANSITION, FOOT_X_CENTER, height, speed, "right")
    combined_transition_phases = [transition_phase_left + transition_phase_right for transition_phase_left, transition_phase_right in zip(transition_phase_left, transition_phase_right)]

    step_back_phase_left = build_push_phase(direction, FOOT_X_CENTER, height, step_length, speed, "left")
    step_back_phase_right = build_swing_phase(direction, FOOT_X_CENTER, height+1, step_length, speed, "right")
    combined_step_phase = [step_back_phase_left + step_back_phase_right for step_back_phase_left, step_back_phase_right in zip(step_back_phase_left, step_back_phase_right)]

    lean_right_left = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "left")
    lean_right_right = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_right = [lean_right_left + lean_right_right for lean_right_left, lean_right_right in zip(lean_right_left, lean_right_right)]

    #single_step = combined_swing_phases + combined_step_phase
    single_step = combined_lean_left + combined_swing_phases + combined_transition_phases + combined_step_phase + combined_lean_right

    movement_array = []
    for k in range(num_steps):
        movement_array += single_step

    return movement_array

def build_turn_right_array(direction, height, step_length, num_steps, speed):
    lean_left_left = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "left")
    lean_left_right = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_left = [lean_left_left + lean_left_right for lean_left_left, lean_left_right in zip(lean_left_left, lean_left_right)]
    
    swing_phase_left = build_swing_phase(direction, FOOT_X_CENTER+1, height+1, step_length, speed, "left")
    swing_phase_right = build_push_phase(direction, FOOT_X_CENTER-1, height, step_length, speed, "right")
    combined_swing_phases = [swing_phase_left + swing_phase_right for swing_phase_left, swing_phase_right in zip(swing_phase_left, swing_phase_right)]
    
    transition_phase_left = build_lean_phase(TRANSITION, FOOT_X_CENTER, height, speed, "left")
    transition_phase_right = build_lean_phase(TRANSITION, FOOT_X_CENTER, height+1, speed, "right")
    combined_transition_phases = [transition_phase_left + transition_phase_right for transition_phase_left, transition_phase_right in zip(transition_phase_left, transition_phase_right)]

    step_back_phase_left = build_push_phase(direction, FOOT_X_CENTER+1, height, step_length, speed, "left")
    step_back_phase_right = build_swing_phase(direction, FOOT_X_CENTER-1, height, step_length, speed, "right")
    combined_step_phase = [step_back_phase_left + step_back_phase_right for step_back_phase_left, step_back_phase_right in zip(step_back_phase_left, step_back_phase_right)]

    lean_right_left = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "left")
    lean_right_right = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_right = [lean_right_left + lean_right_right for lean_right_left, lean_right_right in zip(lean_right_left, lean_right_right)]

    #single_step = combined_swing_phases + combined_step_phase
    single_step = combined_lean_left + combined_swing_phases + combined_transition_phases + combined_step_phase + combined_lean_right

    movement_array = []
    for k in range(num_steps):
        movement_array += single_step

    return movement_array

def build_turn_left_array(direction, height, step_length, num_steps, speed):
    lean_left_left = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "left")
    lean_left_right = build_lean_phase(LEFT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_left = [lean_left_left + lean_left_right for lean_left_left, lean_left_right in zip(lean_left_left, lean_left_right)]
    
    swing_phase_left = build_swing_phase(direction, FOOT_X_CENTER-1, height+1, step_length, speed, "left")
    swing_phase_right = build_push_phase(direction, FOOT_X_CENTER+1, height, step_length, speed, "right")
    combined_swing_phases = [swing_phase_left + swing_phase_right for swing_phase_left, swing_phase_right in zip(swing_phase_left, swing_phase_right)]
    
    transition_phase_left = build_lean_phase(TRANSITION, FOOT_X_CENTER, height, speed, "left")
    transition_phase_right = build_lean_phase(TRANSITION, FOOT_X_CENTER, height, speed, "right")
    combined_transition_phases = [transition_phase_left + transition_phase_right for transition_phase_left, transition_phase_right in zip(transition_phase_left, transition_phase_right)]

    step_back_phase_left = build_push_phase(direction, FOOT_X_CENTER-1, height, step_length, speed, "left")
    step_back_phase_right = build_swing_phase(direction, FOOT_X_CENTER+1, height+1, step_length, speed, "right")
    combined_step_phase = [step_back_phase_left + step_back_phase_right for step_back_phase_left, step_back_phase_right in zip(step_back_phase_left, step_back_phase_right)]

    lean_right_left = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "left")
    lean_right_right = build_lean_phase(RIGHT, FOOT_X_CENTER, height, speed, "right")
    combined_lean_right = [lean_right_left + lean_right_right for lean_right_left, lean_right_right in zip(lean_right_left, lean_right_right)]

    #single_step = combined_swing_phases + combined_step_phase
    single_step = combined_lean_left + combined_swing_phases + combined_transition_phases + combined_step_phase + combined_lean_right

    movement_array = []
    for k in range(num_steps):
        movement_array += single_step

    return movement_array

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

def load_positions_from_ini(file_path):
    """
    Reads a custom profile .ini file and returns a list of angle arrays.
    Example line format:
        Position1: [90, 45, 120, 88, 90, 110, 90, 45, 120, 88, 90, 110]
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    positions = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            # Only process lines that start with "Position"
            if line.startswith("Position"):
                try:
                    # Extract the list inside brackets
                    raw_list = line.split(":", 1)[1].strip()
                    angle_list = eval(raw_list)  # safe here because it's your own file format

                    if isinstance(angle_list, list) and len(angle_list) == 12:
                        positions.append(angle_list)
                except Exception as e:
                    print(f"Error parsing line: {line}")
                    print(e)

    return positions

def build_custom_profile_from_positions(positions, speed):
    """
    Takes a list of 12‑angle arrays and converts them into a smooth movement profile.
    Each transition between positions is interpolated based on speed.
    """
    if not positions:
        print("No positions provided.")
        return []

    movement_profile = []

    # Convert speed to number of frames per transition
    frames = convert_speed_to_frames(speed)

    # Start at first position
    prev = positions[0]
    movement_profile.append(prev)

    # Interpolate between each pair of positions
    for next_pos in positions[1:]:
        transition_frames = []

        for t in np.linspace(0, 1, frames):
            frame = []
            for i in range(12):
                # Linear interpolation between prev[i] and next_pos[i]
                val = prev[i] + (next_pos[i] - prev[i]) * t
                frame.append(round(val, 2))
            transition_frames.append(frame)

        movement_profile.extend(transition_frames)
        prev = next_pos

    return movement_profile

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