import sys
import time

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/')

from _firmware.instruments import servo_utility
from _firmware.robot import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *
from equipment.ssh_tx_comms import *
from equipment.serial_comms import *
from utilities.write_to_file import *
from utilities.kinematics import *
from utilities.movement_profiles import *

DEBUG_PRINT_STATEMENT = False

ssh_shell = False
ssh_connection = False
rf_connection = False

def check_is_none(angles, last_angles, leg):
    if angles is None:
        angles = [90, 90, 90, 90, 90, 90]
        for k in range(6):
            if leg == "right":
                angles[k] = last_angles[k+6]
            else:
                angles[k] = last_angles[k]
    return angles

def send_leg_commands_to_robot(robot, simulate, last_all_leg_angles, all_leg_angles):
    global tx, serials, rf_connection, ssh_connection

    try:
        if simulate:
            robot.set_all_angles(all_leg_angles)
            robot.update()
            return all_leg_angles  # update and return new state

        for k in range(NUMBER_OF_SERVOS):
            if last_all_leg_angles[k] != all_leg_angles[k]:
                cmd = f"CMD {ID} {ALL_LEG_NAMES[k]} {all_leg_angles[k]}"
                if rf_connection:
                    response = serials.send_command(cmd)
                else:
                    tx.send_user_input(f"{ALL_LEG_NAMES[k]}{all_leg_angles[k]}\n")

        if ssh_connection:
            response = tx.receive_response()
            if response:
                print(response)

        return all_leg_angles  # update and return new state

    except Exception as e:
        print("Sending command error...")
        print(e)
        return last_all_leg_angles  # fallback to previous state

def run_movement_profile(mc_gui, robot, simulate, last_angles, movement_array):
    # TODO this will execute the entirety of movement array
    # NOTE you will be locked into movement profile until it is complete
    for k in range(len(movement_array)):
        mc_gui.set_all_slider_angles(movement_array[k])
        send_leg_commands_to_robot(robot, simulate, last_angles, movement_array[k])
        last_angles = movement_array[k]
        #time.sleep(0.001)

    return last_angles

def run_kinematics(mc_gui, last_angles, mode):
    if mode == "Angles":
        # TODO this is bugged out and doesnt work as intended
        #print("Loading Angle Control...")
        leg_angles = mc_gui.get_all_slider_angles()
        left_leg_pos = compute_forward_kinematics(leg_angles, "left")
        right_leg_pos = compute_forward_kinematics(leg_angles, "right")
        mc_gui.set_all_slider_pos(left_leg_pos + right_leg_pos)
        # TODO compute forward kinematics and set pos values 
        #print(leg_angles)

    elif mode == "Kinematics":
        #print("Loading Kinematic Control...")
        leg_pos = mc_gui.get_all_slider_pos()  
        #print("Leg Pos...", leg_pos) 
        left_leg_angles = compute_inverse_kinematics(leg_pos[0], leg_pos[1], leg_pos[2], "left")
        right_leg_angles = compute_inverse_kinematics(leg_pos[3], leg_pos[4], leg_pos[5], "right")

        left_leg_angles = check_is_none(left_leg_angles, last_angles, "left")
        right_leg_angles = check_is_none(right_leg_angles, last_angles, "right")
        leg_angles = left_leg_angles + right_leg_angles

        mc_gui.set_all_slider_angles(leg_angles)

    return leg_angles

def run_manual_control_api(simulate, recal_servos):
    global tx
    global serials
    global rf_connection

    last_all_leg_angles = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
    standing_array = [[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]]

    if simulate:
        # go thru local firmware folder to create objects
        pca = servo_utility.PCA9865(0x41, simulate)
        robot = Robot(pca, recal_servos)
    else:
        robot = None
        # Run manual control on robot firmware
        tx.run_manual_control(FIRMWARE_REMOTE_LOCATION, rf_connection, recal_servos)
    
    if recal_servos:
        starting_leg_pos = last_all_leg_angles  # Set all angles to 90
        standing_array[0] = starting_leg_pos
    
    else:
        standing_array = build_stand_still_array(WALKING_HEIGHT)
        left_leg_pos = compute_forward_kinematics(standing_array[0], "left")
        right_leg_pos = compute_forward_kinematics(standing_array[0], "right")
        starting_leg_pos = left_leg_pos + right_leg_pos

    manual_control_gui = Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT, standing_array[0], starting_leg_pos, recal_servos)

    running = True
    while running:
        
        running, button = manual_control_gui.update()
        if button == "recal_servos":
            if not recal_servos:
                print("Writing Cal Data to file...")
                write_cal_data(last_all_leg_angles)
            else:
                print("Simulate mode does not allow overwrite of cal data")

        elif button == "stand":
            print("Setting Standing Position")
            
            movement_array = build_stand_still_array(WALKING_HEIGHT)
            last_all_leg_angles = run_movement_profile(manual_control_gui, robot, simulate, last_all_leg_angles, movement_array)

        elif button == "walk_forward":
            print("Walking Forward...")
            movement_array = build_walk_array(1, WALKING_HEIGHT, 2, 1)
            last_all_leg_angles = run_movement_profile(manual_control_gui, robot, simulate, last_all_leg_angles, movement_array)

        elif button == "walk_backward":
            print("Walking Backward...")
            movement_array = build_walk_array(-1, WALKING_HEIGHT, 2, 1)
            last_all_leg_angles = run_movement_profile(manual_control_gui, robot, simulate, last_all_leg_angles, movement_array)

        else:
            pass

        try:
            mode = manual_control_gui.get_mode()

            all_leg_angles = run_kinematics(manual_control_gui, last_all_leg_angles, mode)
            last_all_leg_angles = send_leg_commands_to_robot(robot, simulate, last_all_leg_angles, all_leg_angles)
           
        except Exception as e:
            print(e)
            return 'exit'

    return button

def run_firmware(tx):
    global ssh_shell

    tx.run_firmware(FIRMWARE_REMOTE_LOCATION)
    ssh_shell = True

def test_accelerometer(tx):
    global ssh_shell
    global DEBUG_PRINT_STATEMENT

    DEBUG_PRINT_STATEMENT = True
    tx.run_test(ACCELEROMETER_REMOTE_LOCATION, ACCELEROMETER)
    ssh_shell = True

def run_connect_ssh():
    global ssh_connection 
    
    ssh_connection = tx.connect_ssh()

def run_connect_nrf():
    global serials
    global rf_connection
    
    serials_connection = serials.connect()

    if serials_connection:
        try:
            joint, rf_connection = serials.send_command("CMD 39 STA 1.0") # Check status of LED
            #print(rf_connection)
        except:
            print("No acknowledgement received from humanoid receiver!")
   
def close_all():
    global serials

    serials_connection = serials.connect()

    if serials_connection:

        serials.send_command("CMD 39 DIS 0.0")
        serials.close()

def run_startup_control_api():
    global tx 
    global serials
    global ssh_shell
    global ssh_connection
    global rf_connection

    start_gui = Startup_GUI(GUI_WIDTH, GUI_HEIGHT, HOSTNAME, USERNAME, FIRMWARE_REMOTE_LOCATION, COM_PORT, BAUDRATE)
    tx = SSH_TX_Comms(HOSTNAME, USERNAME, PASSWORD, FIRMWARE_REMOTE_LOCATION)
    serials = Serial_Comms(port=COM_PORT, baudrate=BAUDRATE)
    
    dispatch = {
    "ssh": lambda: run_connect_ssh(),
    "nrf": lambda: run_connect_nrf(),
    "send": lambda: tx.send_command(start_gui.get_command()),
    "firmware": lambda: tx.install_firmware(FIRMWARE_LOCAL_LOCATION, FIRMWARE_REMOTE_LOCATION),
    "run_firmware": lambda: run_firmware(tx),
    "test_accelerometer": lambda: test_accelerometer(tx),
    "uninstall_firmware": lambda: tx.uninstall_firmware(FIRMWARE_REMOTE_LOCATION),
    "raspi_config": lambda: tx.run_config(FIRMWARE_REMOTE_LOCATION),
    "reboot": lambda: tx.run_reboot(FIRMWARE_REMOTE_LOCATION)
    }
    
    running = True
    while running:
        simulate = start_gui.get_simulate_value()
        recal_servos = start_gui.get_recal_value()

        running, button = start_gui.update(ssh_connection, rf_connection)

        action = dispatch.get(button)
        if action:
            action()

        if ssh_shell:
            response = tx.receive_response()
            if response and DEBUG_PRINT_STATEMENT:
                print(response)
    return button, simulate, recal_servos
        
if __name__ == "__main__":
    pressed_button = "start"

    while pressed_button != "exit":
        if pressed_button == "start":
            pressed_button, simulate, recal_servos = run_startup_control_api()

        elif pressed_button == "manual_control":
            pressed_button = run_manual_control_api(simulate, recal_servos)

    close_all()

    