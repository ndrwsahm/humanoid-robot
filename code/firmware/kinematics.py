import math
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

        # Hip Extendor
        """ Extra angle may need later
        equation_str = f"({A1_LENGTH}*{A1_LENGTH} + {D}*{D} - {A2_LENGTH}*{A2_LENGTH}) / (2 * {A1_LENGTH} * {D})"
        err = "hip_beta domain error!!"

        numerator = (A1_LENGTH*A1_LENGTH + D*D - A2_LENGTH*A2_LENGTH)
        denomenator = (2 * A1_LENGTH * D)
      
        if numerator > denomenator:
            hip_beta = 0
        else:
            hip_beta = math.acos(numerator / denomenator)
            hip_beta = math.degrees(hip_beta)
        """

        equation_str = f"(acos ({x} / {A1_LENGTH}))"
        err = "hip_alpha domain error!!"

        if x >= A1_LENGTH:
            hip_alpha = 0
        elif x <= -A1_LENGTH:
            hip_alpha = 180
        else:
            hip_alpha = math.acos(x / A1_LENGTH)
            hip_alpha = math.degrees(hip_alpha)
    
        hip_extendor = hip_alpha  # for left or right need to subtract 180 - alpha respectively

        # Side Plane Kinematics================================
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
        """ Extra angle may need later
        ankle_beta = math.acos((A2_LENGTH*A2_LENGTH + D*D - A1_LENGTH*A1_LENGTH) / (2 * A2_LENGTH * D))
        ankle_beta = math.degrees(ankle_beta)
        equation_str = f"({A2_LENGTH}*{A2_LENGTH} + {D}*{D} - {A1_LENGTH}*{A1_LENGTH}) / (2 * {A2_LENGTH} * {D})"
        err = "ankle_beta domain error!!"
        """

        ankle_alpha = math.acos(x / D)
        equation_str = f"(acos ({x} / {D})_"
        ankle_alpha = math.degrees(ankle_alpha)
        err = "ankle_alpha domain error!!"

        ankle_extendor = ankle_alpha   # for left or right need to subtract 180 - alpha respectively

        # Front Plane Kinematics
        # TODO assuming y = 0 for now until solid

        theta = [90, 90, hip_extendor, knee_extendor, 90, ankle_extendor]      # hip rotation independent of kinematics

        # TODO check max thetas and limit values

    except Exception as e:
        print(e)
        print("Equation = " + equation_str)
        print(err)
    
    return theta

def compute_forward_kinematics(theta1, theta2, theta3):
    x = 0
    y = 0
    z = 0

    return [x, y, z]

joint_names = [
    "Hip Rotator",
    "Hip Abductor",
    "Hip Extendor",
    "Knee Extendor",
    "Ankle Abductor",
    "Ankle Extendor"
]

x_pos = -5
y_pos = 0
z_pos = 18

angles = compute_inverse_kinematics(x_pos, y_pos, z_pos)

print(f"    X:    |    Y:    |    Z:   ")
print("-" * 35)
print(f"    {x_pos}     |    {y_pos}     |    {z_pos}")
print("")
# Print header
print(f"{'Joint':<20} | {'Angle (°)'}")
print("-" * 35)

# Print each joint and its angle
for name, angle in zip(joint_names, angles):
    print(f"{name:<20} | {angle:>8.2f}")

