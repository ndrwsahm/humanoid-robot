import sys

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/')

from _firmware.instruments import servo_utility
from _firmware.robot import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *
from equipment.ssh_tx_comms import *
from equipment.serial_comms import *
from utilities.write_to_file import *
from utilities.kinematics import *

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

def run_kinematics(mc_gui, last_angles, mode):
    if mode == "Angles":
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

    last_all_leg_angles = [90,90,90,90,90,90,90,90,90,90,90,90]

    if simulate:
        # go thru local firmware folder to create objects
        pca = servo_utility.PCA9865(0x41, simulate)
        robot = Robot(pca, recal_servos)
    else:
        # TODO how are you going to run firmware via RF????? FUCK.... also RF keeps crashing due to parsing issues, will randomly receive 000000000 instead of lha 180.0
        tx.run_manual_control(FIRMWARE_REMOTE_LOCATION, rf_connection, recal_servos)
    
    manual_control_gui = Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT, recal_servos)

    running = True
    while running:
        
        running, button = manual_control_gui.update()

        # TODO create write file 
        if button == "recal_servos":
            print("Writing Cal Data to file...")
            write_cal_data(last_all_leg_angles)

        try:
            mode = manual_control_gui.get_mode()

            all_leg_angles = run_kinematics(manual_control_gui, last_all_leg_angles, mode)

            if simulate:
                # go thru local firmware folder to create objects
                #print("Setting Angles...")
                robot.set_all_angles(all_leg_angles)
                #print("Updating Robot...")
                robot.update()
                last_all_leg_angles = all_leg_angles
            
            else:
                try:
                    for k in range(NUMBER_OF_SERVOS):
                        if last_all_leg_angles[k] != all_leg_angles[k]:
                            if rf_connection:
                                response = serials.send_command("CMD " + str(ID) + " " + ALL_LEG_NAMES[k] + " " + str(all_leg_angles[k]))
                            else:
                                tx.send_user_input(ALL_LEG_NAMES[k] + str(all_leg_angles[k]) + "\n")

                    # check response
                    if ssh_connection:
                        response = tx.receive_response()
                        if response:
                            print(response)
                    last_all_leg_angles = all_leg_angles
                except Exception as e:
                    print("Sending command error...")
                    print (e)
        except:
            return 'exit'

    return button

def run_firmware(tx):
    global ssh_shell

    tx.run_firmware(FIRMWARE_REMOTE_LOCATION)
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
            joint, rf_connection = serials.send_command("CMD 39 STA 0.0") # Check status of LED
        except:
            print("No acknowledgement received from humanoid receiver!")
   
        #serials.close()

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
            if response:
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

    