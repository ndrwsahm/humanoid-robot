from robot import *
from instruments.serial_rx_comms import * 
from instruments.ssh_rx_comms import *
from instruments.servo_utility import *

running = True
DEBUG_PRINT_STATEMENT = False

def parse_user_input(user_input):
    global joint_map

    joint = user_input[:3]
    angle_str = user_input[3:].strip()
    try:
        angle = float(angle_str)
    except ValueError:
        print("Error in parsing input, setting default angle...")
        angle = 999  # Default fallback if angle is malformed

    servo = joint_map.get(joint, -1)  # -1 if joint not found
    
    if DEBUG_PRINT_STATEMENT:
        print (" ")
        print("User Input: " + user_input)

        print("Servo: " + str(servo))
        print("Angle: " + str(angle))

    return servo, angle

if __name__ == "__main__":
    print("Hello User!")

    try:
        pca_obj = PCA9865(0x41, False)
        print("Creating Robot Object...")
        robot = Robot(pca_obj, True)
        print("True")

        #           lhr, lha, lhe, lk, laa, lae
        #robot.set_all_angles([90,80,60,100,100,70,90,100,120,90,100,100])
        print("Using STDIN for command input...")
        rx_comms = SSH_RX_Comms()  # but modify SSH_RX_Comms to rea
        
    except Exception as e:
        print(e)

    # Hardcoded soft start angles
    all_angles = N90_DEGREE_START_ANGLES
    robot.set_all_angles(N90_DEGREE_START_ANGLES)

    while running:
        user_input = rx_comms.get_user_input()
        if user_input:
            servo, angle = parse_user_input(user_input)
            
            if servo >= 0 and angle != 999:
                all_angles[servo] = angle
                #           lhr, lha, lhe, lk, laa, lae
                robot.set_all_angles(all_angles)
            else:
                robot.set_all_angles(N90_DEGREE_START_ANGLES)

