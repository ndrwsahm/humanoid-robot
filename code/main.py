import sys

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/firmware/instruments')

from firmware.instruments import servo_utility
from firmware.robot import *
from firmware.kinematics import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *
from ssh_tx_comms import *

def run_manual_control_api(simulate):
    global tx
    last_all_leg_angles = [90,90,90,90,90,90,90,90,90,90,90,90]

    if simulate:
        # go thru local firmware folder to create objects
        pca = servo_utility.PCA9865(0x41, simulate)
        robot = Robot(pca)
    else:
        tx.run_manual_control(FIRMWARE_REMOTE_LOCATION)
        
    manual_control_gui = Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT)
    # TODO, no access to robot bc thats firmware
    #starting_angles = robot.get_all_angles()
    #manual_control_gui.new(starting_angles)

    running = True
    while running:
        
        running, button = manual_control_gui.update()

        try:
            mode = manual_control_gui.get_mode()

            if mode == "Angles":
                all_leg_angles = manual_control_gui.get_all_slider_angles()
                left_leg_pos = compute_forward_kinematics(all_leg_angles, "left")
                right_leg_pos = compute_forward_kinematics(all_leg_angles, "right")
                manual_control_gui.set_all_slider_pos(left_leg_pos + right_leg_pos)
                # TODO compute forward kinematics and set pos values 
                #print(all_leg_angles)

            elif mode == "Kinematics":
                all_leg_pos = manual_control_gui.get_all_slider_pos()   
                left_leg_angles = compute_inverse_kinematics(all_leg_pos[0], all_leg_pos[1], all_leg_pos[2])
                right_leg_angles = compute_inverse_kinematics(all_leg_pos[3], all_leg_pos[4], all_leg_pos[5])
                manual_control_gui.set_all_slider_angles(left_leg_angles + right_leg_angles)
                
            # TODO delete when mode select is finished
            all_leg_angles = manual_control_gui.get_all_slider_angles()

            if simulate:
                # go thru local firmware folder to create objects
                robot.set_all_angles(all_leg_angles)

                robot.update()
            
            else:
                try:
                    # if connected send all angles positions to pi
                    if last_all_leg_angles[0] != all_leg_angles[0]:
                        tx.send_user_input("lhr" + str(all_leg_angles[0]) + "\n")
                    if last_all_leg_angles[1] != all_leg_angles[1]:
                        tx.send_user_input("lha" + str(all_leg_angles[1]) + "\n")
                    if last_all_leg_angles[2] != all_leg_angles[2]:
                        tx.send_user_input("lhe" + str(all_leg_angles[2]) + "\n")
                    if last_all_leg_angles[3] != all_leg_angles[3]:
                        tx.send_user_input("lkk" + str(all_leg_angles[3]) + "\n")
                    if last_all_leg_angles[4] != all_leg_angles[4]:
                        tx.send_user_input("laa" + str(all_leg_angles[4]) + "\n")
                    if last_all_leg_angles[5] != all_leg_angles[5]:
                        tx.send_user_input("lae" + str(all_leg_angles[5]) + "\n")
                    if last_all_leg_angles[6] != all_leg_angles[6]:
                        tx.send_user_input("rhr" + str(all_leg_angles[6]) + "\n")
                    if last_all_leg_angles[7] != all_leg_angles[7]:
                        tx.send_user_input("rha" + str(all_leg_angles[7]) + "\n")
                    if last_all_leg_angles[8] != all_leg_angles[8]:
                        tx.send_user_input("rhe" + str(all_leg_angles[8]) + "\n")
                    if last_all_leg_angles[9] != all_leg_angles[9]:
                        tx.send_user_input("rkk" + str(all_leg_angles[9]) + "\n")
                    if last_all_leg_angles[10] != all_leg_angles[10]:
                        tx.send_user_input("raa" + str(all_leg_angles[10]) + "\n")
                    if last_all_leg_angles[11] != all_leg_angles[11]:
                        tx.send_user_input("rae" + str(all_leg_angles[11]) + "\n")
                    response = tx.receive_response()
                    if response:
                        print(response)
                    last_all_leg_angles = all_leg_angles
                except Exception as e:
                    print (e)
        except:
            return 'exit'

    return button

def run_startup_control_api():
    global tx 

    start_gui = Startup_GUI(GUI_WIDTH, GUI_HEIGHT, HOSTNAME, USERNAME, FIRMWARE_REMOTE_LOCATION)
    tx = SSH_TX_Comms(HOSTNAME, USERNAME, PASSWORD, FIRMWARE_REMOTE_LOCATION)
    connection = False
    ssh_shell = False
    running = True
    while running:
        simulate = start_gui.get_simulate_value()
        running, button = start_gui.update(connection)
        if button == "ssh":
            connection = tx.connect_ssh()
        elif button == "send":
            command = start_gui.get_command()
            tx.send_command(command)
        elif button == "test_comms":
            if simulate:
                pass
            else:
                tx.test_comms()
        elif button == "firmware":
            tx.install_firmware(FIRMWARE_LOCAL_LOCATION, FIRMWARE_REMOTE_LOCATION)
        elif button == "run_firmware":
            tx.run_firmware(FIRMWARE_REMOTE_LOCATION)
            ssh_shell = True
        elif button == "uninstall_firmware":
            tx.uninstall_firmware(FIRMWARE_REMOTE_LOCATION)
        elif button == "raspi_config":
            tx.run_config(FIRMWARE_REMOTE_LOCATION)
        elif button == "reboot":
            tx.run_reboot(FIRMWARE_REMOTE_LOCATION)

        if ssh_shell:
            response = tx.receive_response()
            if response:
                print(response)
    return button, simulate
        
if __name__ == "__main__":
    pressed_button = "start"

    while pressed_button != "exit":
        if pressed_button == "start":
            pressed_button, simulate = run_startup_control_api()

        elif pressed_button == "manual_control":
            pressed_button = run_manual_control_api(simulate)

    