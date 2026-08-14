import math
import numpy as np
import sys
import os
from globals import *

from _firmware.utility_functions.settings_parser import load_robot_settings

firmware_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, firmware_dir)

from _firmware.firmware_globals import *

settings = load_robot_settings(ID)

A1_LENGTH = settings["A1_LENGTH"]
A2_LENGTH = settings["A2_LENGTH"]
A3_LENGTH = settings["A3_LENGTH"]
A4_LENGTH = settings["A4_LENGTH"]

import math

def compute_inverse_arm_kinematics(x, y, z, arm):
    """
    IK for:
    - Shoulder yaw (rotator)
    - Shoulder pitch (extender)
    - Elbow pitch (mounted 90 degrees from shoulder pitch)

    Parameters:
        x, y, z : target position in torso frame
        arm     : "left" or "right"

    Returns:
        yaw_deg, shoulder_pitch_deg, elbow_pitch_deg
    """

    # -----------------------------------------
    # 1. SHOULDER YAW (normal)
    # -----------------------------------------
    yaw = math.atan2(y, x)

    # Rotate target into shoulder pitch plane
    r = math.sqrt(x**2 + y**2)
    px = r
    pz = z

    # -----------------------------------------
    # 2. ELBOW IK (2-link planar)
    # -----------------------------------------
    D = (px**2 + pz**2 - A3_LENGTH**2 - A4_LENGTH**2) / (2 * A3_LENGTH * A4_LENGTH)
    D = max(min(D, 1.0), -1.0)  # clamp

    # Standard elbow angle
    elbow = math.acos(D)

    # -----------------------------------------
    # 3. SHOULDER PITCH
    # -----------------------------------------
    phi = math.atan2(pz, px)
    psi = math.atan2(A4_LENGTH * math.sin(elbow),
                     A3_LENGTH + A4_LENGTH * math.cos(elbow))

    shoulder_pitch = phi - psi

    # Convert to degrees
    return [math.degrees(yaw), math.degrees(shoulder_pitch), math.degrees(elbow)]

import math

def compute_forward_arm_kinematics(angles, arm):
    """
    Forward kinematics for:
    - Shoulder yaw
    - Shoulder pitch
    - Elbow pitch (mounted 90 degrees offset)

    Parameters:
        angles  : [yaw_deg, shoulder_pitch_deg, elbow_pitch_deg]
        arm           : "left" or "right"

    Returns:
        x, y, z  (end-effector position)
    """

    # Convert to radians
    yaw = math.radians(angles[0])
    shoulder = math.radians(angles[1])

    # Elbow is mounted 90° rotated
    elbow = math.radians(angles[2] + 90)

    # -----------------------------------------
    # 1. Compute planar extension in shoulder plane
    # -----------------------------------------
    # Upper arm contribution
    x1 = A3_LENGTH * math.cos(shoulder)
    z1 = A3_LENGTH * math.sin(shoulder)

    # Forearm contribution
    x2 = A4_LENGTH * math.cos(shoulder + elbow)
    z2 = A4_LENGTH * math.sin(shoulder + elbow)

    # Total reach in shoulder plane
    px = x1 + x2
    pz = z1 + z2

    # -----------------------------------------
    # 2. Rotate by shoulder yaw to get full 3D
    # -----------------------------------------
    x = px * math.cos(yaw)
    y = px * math.sin(yaw)
    z = pz

    return x, y, z

def compute_inverse_leg_kinematics(x, y, z, leg):
    # Assumptions: Moving COM by abductors does not effect height of robot
        
    if x == 0:
        x = 0.001
    if y == 0:
        y = 0.001
    if z == 0:
        z = 0.001

    try:
        # Side View Kinematics =========================================================================
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
            if leg == "left":
                knee_extendor = 180 - math.degrees(knee_extendor)
            else:
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

        if leg == "left":
            ankle_extendor = ankle_alpha + ankle_beta 
        else:
            ankle_extendor = 180 - (ankle_alpha + ankle_beta)

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

        if leg == "left":
            hip_extendor = hip_alpha - hip_beta
        else:
            hip_extendor = 180 - (hip_alpha - hip_beta)

        # Front View Kinematics =========================================================================
        hip_abductor = math.acos(y/D)
        hip_abductor = math.degrees(hip_abductor)
        hip_abductor = 180 - hip_abductor

        ankle_abductor = hip_abductor

        theta = [90, hip_abductor, hip_extendor, knee_extendor, ankle_abductor, ankle_extendor]      # hip rotation independent of kinematics
        # TODO check max thetas and limit values

    except Exception as e:
        print(e)
        print("Equation = " + equation_str)
        print(err)
        return None # handle error upstream

    return theta

def compute_forward_leg_kinematics(angles, leg):
    """
    Compute planar forward kinematics for a leg (side view).
    Returns (x, z) in same length units as A1, A2.

    Parameters
    - angles: [hip_deg, knee_deg] in degrees
    - leg: "left" or "right"
    - deg_input: True if input angles are degrees (default True)
    - mirror_right: if True, apply the same mirroring convention used in your code
      (e.g., if right-leg angles are stored mirrored as 180 - angle). Set False if
      angles are already in servo/joint space.
    """
    hip = angles[HE_IDX]  # Assuming hip is the first angle in the list
    abductor = angles[HA_IDX] # Assuming abductor is the second angle in the list
    knee = angles[KK_IDX] # Assuming knee is the second angle in the list

    # If your project stores right-leg angles mirrored (e.g., 180 - angle),
    # undo that mirroring here when computing forward kinematics.
    if leg == "right":
        # Example mirroring convention: convert mirrored representation to actual joint angles
        hip = math.radians(180.0 - hip)
        knee = math.radians(180.0 - knee)
        abductor = math.radians(180.0 - abductor)
    else:
        hip = math.radians(hip)
        knee = math.radians(knee)
        abductor = math.radians(abductor)

    # knee position relative to hip
    knee_x = A1_LENGTH * math.cos(hip)
    knee_z = -A1_LENGTH * math.sin(hip)

    # foot relative to knee
    foot_x = A2_LENGTH * math.cos(hip + knee)
    foot_z = -A2_LENGTH * math.sin(hip + knee)

    # total foot position
    x = knee_x + foot_x
    z = knee_z + foot_z

    y = z * math.cos(abductor)  # Adjust y based on abductor angle
  
    return x,y,z


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
    z_pos = -12

    angles = compute_inverse_leg_kinematics(x_pos, y_pos, z_pos, "right")

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

    x_pos, y_pos, z_pos = compute_forward_leg_kinematics(angles, "right")

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
    
