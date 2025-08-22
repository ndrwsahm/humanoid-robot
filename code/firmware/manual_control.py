from robot import *
from instruments.rx_comms import * 
from instruments.servo_utility import *

running = True

def parse_user_input(user_input):
    # [lhr, lha, lhe, lk, laa, lae, rhr, rha, rhe, rk, raa, rae]
    angle = int(user_input[3:])
    #print(user_input[3:])
    input = user_input[0:3]
    #angle = 90
    if input == "lhr":
        servo = 0
    elif input == "lha":
        servo = 1
    elif input == "lhe":
        servo = 2
    elif input == "lkk":
        servo = 3
    elif input == "laa":
        servo = 4
    elif input == "lae":
        servo = 5
    elif input == "rhr":
        servo = 6
    elif input == "rha":
        servo = 7
    elif input == "rhe":
        servo = 8
    elif input == "rkk":
        servo = 9
    elif input == "raa":
        servo = 10
    elif input == "rae":
        servo = 11
    else:
        servo = -1
        angle = 90

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
