from robot import *
from instruments.serial_rx_comms import * 
from instruments.ssh_rx_comms import *
from instruments.servo_utility import *

running = True

def parse_user_input(user_input):
    global joint_map

    print (" ")
    print("User Input: " + user_input)

    joint = user_input[:3]
    angle_str = user_input[3:].strip()
    try:
        angle = float(angle_str)
        print("got here")
    except ValueError:
        print("Error in parsing input, setting default angle...")
        angle = 90  # Default fallback if angle is malformed

    servo = joint_map.get(joint, -1)  # -1 if joint not found

    print("Servo: " + str(servo))
    print("Angle: " + str(angle))

    return servo, angle

if __name__ == "__main__":
    print("Hello User!")

    try:
        pca_obj = PCA9865(0x41, False)
        print("Creating Robot Object...")
        if(sys.argv[2] == "recal"):
            robot = Robot(pca_obj, True)
            print("True")
        else:
            robot = Robot(pca_obj, False)
            print("False")
        #           lhr, lha, lhe, lk, laa, lae
        #robot.set_all_angles([90,80,60,100,100,70,90,100,120,90,100,100])
        if(sys.argv[1] == "ssh"):
            print("Creating SSH Comms Object...")
            rx_comms = SSH_RX_Comms()
        else:
            print("Creating RF Comms Object...")
            rx_comms = Serial_RX_Comms()
        
        
    except Exception as e:
        print(e)

    #robot.set_standing_pos()
    #all_angles = robot.get_all_angles()
    all_angles = [90,90,90,90,90,90,90,90,90,90,90,90]
    while running:
        user_input = rx_comms.get_user_input()
        if user_input:
            servo, angle = parse_user_input(user_input)
            
            if servo >= 0:
                all_angles[servo] = angle
                #           lhr, lha, lhe, lk, laa, lae
                robot.set_all_angles(all_angles)

