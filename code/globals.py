import os
import configparser

# PUT GLOBAL ID HERE ====================
ID = 39
# ====================================

# Load configuration file
main_folder = os.path.dirname(__file__)
filename = "configuration.ini"
configuration_folder = os.path.join(main_folder, 'configurations')
id_folder = os.path.join(configuration_folder, str(ID))
full_file_path = os.path.join(id_folder, filename)

config = configparser.ConfigParser()
config.read(full_file_path)

# Set global variables from configuration file
FOOT_X_CENTER = config.getfloat("HUMANOID_VARS", "foot_x_center")
FOOT_Y_SWING = config.getfloat("HUMANOID_VARS", "foot_y_swing")
FOOT_Y_PUSH = config.getfloat("HUMANOID_VARS", "foot_y_push")

WALKING_HEIGHT = config.getfloat("HUMANOID_VARS", "walking_height")

DEFAULT_SPEED = config.getfloat("HUMANOID_VARS", "speed")

# Global variables
ACCELEROMETER = 'accelerometer'
CAMERA = 'camera_sender'

BAUDRATE = 115200
COM_PORT = "COM8"

GUI_WIDTH = 1200
GUI_HEIGHT = 700

NUMBER_OF_SERVOS = 12

FORWARD = 1
BACKWARD = -1

LEFT = 1
TRANSITION = 0
RIGHT = -1

LHR_IDX = 0
LHA_IDX = 1
LHE_IDX = 2
LK_IDX = 3
LAA_IDX = 4
LAE_IDX = 5

RHR_IDX = 6
RHA_IDX = 7
RHE_IDX = 8
RK_IDX = 9
RAA_IDX = 10
RAE_IDX = 11

LEFT_FOOT_X = 0
LEFT_FOOT_Y = 1
LEFT_FOOT_Z = 2

RIGHT_FOOT_X = 3
RIGHT_FOOT_Y = 4
RIGHT_FOOT_Z = 5

SHIFT_WEIGTH_MIN = -7
SHIFT_WEIGTH_MAX = 7
SHIFT_HEIGTH_MIN = -20
SHIFT_HEIGTH_MAX = -4

ALL_LEG_NAMES = ["lhr", "lha", "lhe", "lkk", "laa", "lae", "rhr", "rha", "rhe", "rkk", "raa", "rae"]
ALL_LEGS = [LHR_IDX, LHA_IDX, LHE_IDX, LK_IDX, LAA_IDX, LAE_IDX, RHR_IDX, RHA_IDX, RHE_IDX, RK_IDX, RAA_IDX, RAE_IDX]
ALL_POS = [LEFT_FOOT_X, LEFT_FOOT_Y, LEFT_FOOT_Z, RIGHT_FOOT_X, RIGHT_FOOT_Y, RIGHT_FOOT_Z]
MIN_POS = [-20, SHIFT_WEIGTH_MIN, SHIFT_HEIGTH_MIN, -20, SHIFT_WEIGTH_MIN, SHIFT_HEIGTH_MIN]
MAX_POS = [20, SHIFT_WEIGTH_MAX, SHIFT_HEIGTH_MAX, 20, SHIFT_WEIGTH_MAX, SHIFT_HEIGTH_MAX]

FORWARD = 1
BACKWARD = -1

SPEED = 50

# Pygame Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700