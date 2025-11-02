from robot import *
from instruments.serial_rx_comms import * 
from instruments.ssh_rx_comms import *
from instruments.servo_utility import *

running = True

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
        rx_comms = SSH_RX_Comms()
        
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


