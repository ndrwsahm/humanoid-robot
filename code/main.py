import sys

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/firmware/instruments')

from firmware.instruments import servo_utility
from firmware.robot import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *

def run_manual_control_api(simulate):
    global tx

    if simulate:
        # go thru local firmware folder to create objects
        pca = servo_utility.PCA9865(0x41, simulate)
        robot = Robot(pca)
    else:
        tx.run_firmware(FIRMWARE_REMOTE_LOCATION)
        tx.invoke_shell()
        
    manual_control_gui = Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT)

    running = True
    while running:
        
        running, button = manual_control_gui.update()

        try:
            all_leg_angles = manual_control_gui.get_all_slider_angles()
            if simulate:
                # go thru local firmware folder to create objects
                robot.set_all_angles(all_leg_angles)

                left_leg_pos = robot.left_leg.get_leg_pos()
                right_leg_pos = robot.right_leg.get_leg_pos()

                manual_control_gui.update_pos_labels(left_leg_pos, right_leg_pos)
    
                robot.update()
            
            else:
                # if connected send all angles positions to pi
                tx.send_user_input("lhr" + str(all_leg_angles[0]))
                tx.send_user_input("lha" + str(all_leg_angles[1]))
                tx.send_user_input("lhe" + str(all_leg_angles[2]))
                tx.send_user_input("lk" + str(all_leg_angles[3]))
                tx.send_user_input("laa" + str(all_leg_angles[4]))
                tx.send_user_input("lae" + str(all_leg_angles[5]))
                tx.send_user_input("rhr" + str(all_leg_angles[6]))
                tx.send_user_input("rha" + str(all_leg_angles[7]))
                tx.send_user_input("rhe" + str(all_leg_angles[8]))
                tx.send_user_input("rk" + str(all_leg_angles[9]))
                tx.send_user_input("raa" + str(all_leg_angles[10]))
                tx.send_user_input("rae" + str(all_leg_angles[11]))

        except:
            return 'exit'

    return button

def run_startup_control_api():
    global tx 

    start_gui = Startup_GUI(GUI_WIDTH, GUI_HEIGHT)
    tx = TX_Comms()
    connection = False

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
        elif button == "uninstall_firmware":
            tx.uninstall_firmware(FIRMWARE_REMOTE_LOCATION)
        elif button == "raspi_config":
            tx.run_config(FIRMWARE_REMOTE_LOCATION)
        elif button == "reboot":
            tx.run_reboot(FIRMWARE_REMOTE_LOCATION)

    return button, simulate
        
if __name__ == "__main__":
    pressed_button = "start"

    while pressed_button != "exit":
        if pressed_button == "start":
            pressed_button, simulate = run_startup_control_api()

        elif pressed_button == "manual_control":
            pressed_button = run_manual_control_api(simulate)

    