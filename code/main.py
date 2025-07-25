import sys

sys.path.insert(0, '/Users/andre/Github/humanoid-robot/code/firmware/instruments')

from firmware.instruments import servo_utility
from firmware.robot import *

from GUIs.manual_control_gui import *
from GUIs.startup_gui import *

SIMULATE = True

def run_manual_control_api(robot):
    manual_control_gui = Manual_Control_GUI(GUI_WIDTH, GUI_HEIGHT)

    running = True
    while running:
        
        running, button = manual_control_gui.update()

        try:
            all_leg_angles = manual_control_gui.get_all_slider_angles()

            # TODO will change with wifi connect, change to send all angles
            druid.set_all_angles(all_leg_angles)

            # TODO will change with wifi to connect wifi connections this will need to be send from firmware
            left_leg_pos = robot.left_leg.get_leg_pos()
            right_leg_pos = robot.right_leg.get_leg_pos()

            manual_control_gui.update_pos_labels(left_leg_pos, right_leg_pos)

            # TODO will change with wifi to connect wifi connections this will live on firmware
            druid.update()

        except:
            return 'exit'

    return button

def run_startup_control_api():
    start_gui = Startup_GUI(GUI_WIDTH, GUI_HEIGHT)

    running = True
    while running:
        simulate = start_gui.get_simulate_value()
        running, button = start_gui.update()

    return button, simulate
        
if __name__ == "__main__":
    # TODO wifi setup 
    pressed_button = "start"

    while pressed_button != "exit":
        if pressed_button == "start":
            pressed_button, simulate = run_startup_control_api()

        elif pressed_button == "manual_control":
            pca = servo_utility.PCA9865(0x40, simulate)
            druid = Robot(pca)
            pressed_button = run_manual_control_api(druid)
    