import sys

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/firmware/instruments')

from firmware.instruments import servo_utility
from firmware.robot import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *

def run_manual_control_api(simulate):
    if simulate:
        # go thru local firmware folder to create objects
        pca = servo_utility.PCA9865(0x40, simulate)
        robot = Robot(pca)
    else:
        ssh_comms = TX_Comms()

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
                ssh_comms.send_command("lhr" + str(all_leg_angles[0]))
                ssh_comms.send_command("lha" + str(all_leg_angles[1]))
                ssh_comms.send_command("lhe" + str(all_leg_angles[2]))
                ssh_comms.send_command("lk" + str(all_leg_angles[3]))
                ssh_comms.send_command("laa" + str(all_leg_angles[4]))
                ssh_comms.send_command("lae" + str(all_leg_angles[5]))
                ssh_comms.send_command("rhr" + str(all_leg_angles[6]))
                ssh_comms.send_command("rha" + str(all_leg_angles[7]))
                ssh_comms.send_command("rhe" + str(all_leg_angles[8]))
                ssh_comms.send_command("rk" + str(all_leg_angles[9]))
                ssh_comms.send_command("raa" + str(all_leg_angles[10]))
                ssh_comms.send_command("rae" + str(all_leg_angles[11]))

        except:
            return 'exit'

    return button

def run_startup_control_api():
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

    