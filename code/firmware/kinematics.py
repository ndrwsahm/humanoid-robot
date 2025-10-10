import math
import numpy as np

try:
    from firmware.settings import *
except:
    from settings import *

def compute_inverse_kinematics(x, y, z):
    # Assumptions: Moving COM by abductors does not effect height of robot
    theta = [0, 0, 0, 0, 0, 0]

    if x == 0:
        x = 0.001
    if y == 0:
        y = 0.001
    if z == 0:
        z = 0.001

    try:
        temp = x*x + z*z
        D = math.sqrt(temp)

        # Knee Extendor
        equation_str = f"({A2_LENGTH}*{A2_LENGTH} + {A1_LENGTH}*{A1_LENGTH} - {D}*{D}) / (2 * {A2_LENGTH} * {A1_LENGTH})"
        err = "knee_extendor domain error!!"

        numerator = (A2_LENGTH*A2_LENGTH + A1_LENGTH*A1_LENGTH - D*D)
        denomenator = (2 * A2_LENGTH * A1_LENGTH)
        if numerator > denomenator:
            knee_extendor = 0
        else:
            knee_extendor = math.acos(numerator / denomenator)
            knee_extendor = math.degrees(knee_extendor)

        # Ankle Extendor
        equation_str = f"({A2_LENGTH}*{A2_LENGTH} + {D}*{D} - {A1_LENGTH}*{A1_LENGTH}) / (2 * {A2_LENGTH} * {D})"
        err = "ankle_beta domain error!!"

        numerator = (A2_LENGTH*A2_LENGTH + D*D - A1_LENGTH*A1_LENGTH)
        denomenator = (2 * A2_LENGTH * D)
        if numerator > denomenator:
            ankle_beta = 0
        else:
            ankle_beta = math.acos(numerator / denomenator)
            ankle_beta = math.degrees(ankle_beta)
        
        ankle_alpha = math.acos(x / D)
        equation_str = f"(acos ({x} / {D})_"
        ankle_alpha = math.degrees(ankle_alpha)
        err = "ankle_alpha domain error!!"

        ankle_extendor = 180 - ankle_alpha + ankle_beta   

        # Hip Extendor
        equation_str = f"({A1_LENGTH}*{A1_LENGTH} + {D}*{D} - {A2_LENGTH}*{A2_LENGTH}) / (2 * {A1_LENGTH} * {D})"
        err = "hip_beta domain error!!"

        numerator = (A1_LENGTH*A1_LENGTH + D*D - A2_LENGTH*A2_LENGTH)
        denomenator = (2 * A1_LENGTH * D)
      
        if numerator > denomenator:
            hip_beta = 0
        else:
            hip_beta = math.acos(numerator / denomenator)
            hip_beta = math.degrees(hip_beta)

        hip_alpha = ankle_alpha

        hip_extendor = hip_alpha - hip_beta

        # Front Plane Kinematics
        # TODO assuming y = 0 for now until solid

        theta = [90, 90, hip_extendor, knee_extendor, 90, ankle_extendor]      # hip rotation independent of kinematics

        # TODO check max thetas and limit values

    except Exception as e:
        print(e)
        print("Equation = " + equation_str)
        print(err)
    
    return theta

def compute_forward_kinematics(angles, leg):
    x = 0
    y = 0
    z = 0

    if leg == "left":
        # INFO Ignoring Y pos for now
        knee_x_pos = A1_LENGTH * math.cos(math.radians(angles[LHE_IDX]))
        knee_z_pos = A1_LENGTH * math.sin(math.radians(angles[LHE_IDX]))

        foot_x_pos = A2_LENGTH * math.cos(math.radians(angles[LHE_IDX] + 180 - angles[LK_IDX]))
        foot_z_pos = A2_LENGTH * math.sin(math.radians(angles[LHE_IDX] + 180 - angles[LK_IDX]))

    elif leg == "right":
        knee_x_pos = A1_LENGTH * math.cos(math.radians(angles[RHE_IDX]))
        knee_z_pos = A1_LENGTH * math.sin(math.radians(angles[RHE_IDX]))

        foot_x_pos = A2_LENGTH * math.cos(math.radians(angles[RHE_IDX] + 180 - angles[RK_IDX]))
        foot_z_pos = A2_LENGTH * math.sin(math.radians(angles[RHE_IDX] + 180 - angles[RK_IDX]))

    x = knee_x_pos + foot_x_pos
    z = knee_z_pos + foot_z_pos

    return [x, y, z]

if __name__ == "__main__":
    joint_names = [
        "Hip Rotator",
        "Hip Abductor",
        "Hip Extendor",
        "Knee Extendor",
        "Ankle Abductor",
        "Ankle Extendor"
    ]

    x_pos = 6
    y_pos = 0
    z_pos = -15

    angles = compute_inverse_kinematics(x_pos, y_pos, z_pos)

    print(f"    X:    |    Y:    |    Z:   ")
    print("-" * 35)
    print(f"    {x_pos}     |    {y_pos}     |    {z_pos}")
    
    # Print header
    print(f"{'Joint':<20} | {'Angle (°)'}")
    print("-" * 35)

    # Print each joint and its angle
    for name, angle in zip(joint_names, angles):
        print(f"{name:<20} | {angle:>8.2f}")

    print("")
    print("")

    x_pos, y_pos, z_pos = compute_forward_kinematics(angles)

    # Print header
    print(f"{'Joint':<20} | {'Angle (°)'}")
    print("-" * 35)

    # Print each joint and its angle
    for name, angle in zip(joint_names, angles):
        print(f"{name:<20} | {angle:>8.2f}")

    print(f"    X:    |    Y:    |    Z:   ")
    print("-" * 35)
    print(f"    {x_pos}     |    {y_pos}     |    {z_pos}")
    print("")
    
