from robot import *
from instruments.serial_rx_comms import * 
from instruments.ssh_rx_comms import *
from instruments.servo_utility import *
from utility_functions.settings_parser import load_robot_settings
from utility_functions.username_id import get_robot_id_from_username

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

def check_special_cmd(user_input):
    command = user_input[:3]
    print(f"User Input: {user_input}")
    if command == "scy":
        return True
    elif command == "scn":
        return True
    else:
        return False
    
if __name__ == "__main__":
    print("Hello User!")

    try:
        print("Creating Robot Object...")

        robot = Robot(False)
        #           lhr, lha, lhe, lk, laa, lae
        #robot.set_all_angles([90,80,60,100,100,70,90,100,120,90,100,100])
        print("Using STDIN for command input...")
        rx_comms = SSH_RX_Comms()  # but modify SSH_RX_Comms to rea
        
    except Exception as e:
        print(e)

    robot_id = get_robot_id_from_username()
    settings = load_robot_settings(robot_id)
    
    # Hardcoded soft start angles
    all_angles = settings["SOFT_START_ANGLES"] + settings["SOFT_START_ARM_ANGLES"] + settings["SOFT_START_HEAD_ANGLES"]
    print("Setting soft start angles:", all_angles)
    robot.set_all_angles(all_angles)

    last_roll = 0.0

    while running:
        if robot.is_steady_camera:
            robot.run_steady_camera()

        user_input = rx_comms.get_user_input()

        if user_input:
            
            is_special_cmd = check_special_cmd(user_input)
            
            if is_special_cmd:
                if user_input == "scy":
                    robot.set_steady_camera(True)
                elif user_input == "scn":
                    robot.set_steady_camera(False)
            else:
                print(f"User Input {user_input}")
                servo, angle = parse_user_input(user_input)
                
                if servo >= 0 and angle != 999:
                    all_angles[servo] = angle
                    print("Setting servo {} to angle {}".format(servo, angle))
                    #           lhr, lha, lhe, lk, laa, lae
                    robot.set_all_angles(all_angles)
                else:
                    robot.set_all_angles(settings["SOFT_START_ANGLES"])

