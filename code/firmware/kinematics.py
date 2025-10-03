import math
try:
    from firmware.settings import *
except:
    from settings import *

def compute_inverse_kinematics(self, x, y, z):
    # Assumptions: Moving COM by abductors does not effect height of robot
    theta = [0, 0, 0, 0, 0, 0]

    if x == 0:
        x = 0.001
    if y == 0:
        y = 0.001
    if z == 0:
        z = 0.001

    a = A2_LENGTH
    b = A1_LENGTH

    try:
        temp = x*x + z*z
        c = math.sqrt(temp)

        C = math.acos((a*a + b*b - c*c) / (2 * a * b))
        C = math.degrees(C)

        A = math.acos((b*b + c*c - a*a) / (2 * b * c))
        A = math.degrees(A)

        B = math.acos((a*a + c*c - b*b) / (2 * a * c))
        B = math.degrees(B)

    except Exception as e:
        print(e)
    
    return theta

def compute_forward_kinematics(self, theta1, theta2, theta3):
    x = 0
    y = 0
    z = 0

    return [x, y, z]

def check_work_envelope(self, x, y, z):
    return True
    