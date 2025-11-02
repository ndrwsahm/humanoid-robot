from robot import *
from firmware.instruments.serial_rx_comms import * 
from instruments.servo_utility import *

running = True

joint_map = {
        "lhr": 0, "lha": 1, "lhe": 2, "lkk": 3,
        "laa": 4, "lae": 5, "rhr": 6, "rha": 7,
        "rhe": 8, "rkk": 9, "raa": 10, "rae": 11
    }

def parse_user_input(user_input):
    global joint_map

    joint = user_input[:3]
    try:
        angle = int(user_input[3:])
    except ValueError:
        angle = 90  # Default fallback if angle is malformed

    servo = joint_map.get(joint, -1)  # -1 if joint not found

    return servo, angle

print("Hello User!")

try:
    pca_obj = PCA9865(0x41, False)
    print("Creating Robot Object...")
    robot = Robot(pca_obj)
    #           lhr, lha, lhe, lk, laa, lae
    #robot.set_all_angles([90,80,60,100,100,70,90,100,120,90,100,100])
    print("Creating Comms Object...")
    rx_comms = RX_Comms()
    
except Exception as e:
    print(e)

#robot.set_standing_pos()
#all_angles = robot.get_all_angles()
all_angles = [90,90,90,90,90,90,90,90,90,90,90,90]
while running:
    user_input = rx_comms.get_user_input()
    if user_input:
        print (" ")
        print("User Input   " + user_input)
        servo, angle = parse_user_input(user_input)
        
        if servo >= 0:
            all_angles[servo] = angle
            #           lhr, lha, lhe, lk, laa, lae
            robot.set_all_angles(all_angles)

#while running:
    # TODO Add stuff here 
    #user_input = rx_comms.get_user_input()
    #print(user_input)
    #robot.update()
