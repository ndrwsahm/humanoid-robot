from robot import *
from instruments.rx_comms import * 
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

def setup():
    global pca_obj
    global robot
    global rx_comms

    print("Hello User!")

    try:
        pca_obj = PCA9865(0x41, False)
        print("Creating Robot Object...")
        robot = Robot(pca_obj)

        print("Creating Comms Object...")
        rx_comms = RX_Comms()
        
    except Exception as e:
        print(e)

    robot.set_standing_pos()
    all_angles = robot.get_all_angles()
    time.sleep(1)


if __name__ == "__main__":
    setup()
    
    while running:
        robot.lean_right()
        time.sleep(1)

        robot.stand_right_leg()
        time.sleep(1)

        robot.swing_left_leg()
        time.sleep(1)

        robot.lean_left()
        time.sleep(1)

        robot.stand_left_leg()
        time.sleep(1)

        robot.swing_right_leg()
        time.sleep(1)


