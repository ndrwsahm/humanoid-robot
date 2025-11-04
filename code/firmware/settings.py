PI_COM_PORT = '/dev/ttyUSB0'
PI_BAUDRATE = 115200

A1_LENGTH = 12   # cm
A2_LENGTH = 9.25   # cm

LEFT_LEG_PINS = (8, 9, 10, 11, 12, 13)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
RIGHT_LEG_PINS = (0, 1, 2, 3, 4, 5)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

PULSE_WIDTH_MIN = 0
PULSE_WIDTH_MAX = 1
PULSE_WIDTH_SETTINGS = ((500, 2500), (500, 2500), (500, 2500),  # pins (0, 1, 2)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (3, 4, 5)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (6, 7, 8)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (9, 10, 11)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (12, 13, 14)
                        (500, 2500), (500, 2500), (500, 2500))  # pins (15, 16)

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

HR_IDX = 0
HA_IDX = 1
HE_IDX = 2
KK_IDX = 3
AA_IDX = 4
AE_IDX = 5

LEFT_LEG_DEFAULT_ANGLES = [98.37, 90, 90, 117.21, 77.44, 64.88]
RIGHT_LEG_DEFAULT_ANGLES = [85.81, 94.19, 81.67, 90, 98.37, 146.51]

ANGLES_TO_90 = [90, 90, 90, 90, 90, 90]

LEFT_OFFSET_ANGLES = [x - y for x, y in zip(LEFT_LEG_DEFAULT_ANGLES, ANGLES_TO_90)]
RIGHT_OFFSET_ANGLES = [x - y for x, y in zip(RIGHT_LEG_DEFAULT_ANGLES, ANGLES_TO_90)]

# Hardcoded Angles
STANDING_ANGLES = [82, 88, 71, 73, 77, 94, 90, 96, 105, 134, 103, 121]

LEFT_LEAN_ANGLES = [82, 105, 71, 73, 88, 94, 90, 96, 105, 134, 103, 121]

LEFT_LEG_STAND_ANGLES = [82, 88, 71, 73, 92, 94, 84, 100, 105, 100, 103, 121]

RIGHT_LEG_FORWARD_STEP_ANGLES = [82, 77, 57, 90, 73, 117, 84, 82, 134, 134, 92, 134]

RIGHT_LEAN_ANGLES = [82, 88, 71, 73, 77, 94, 90, 77, 105, 134, 94, 121]

RIGHT_LEG_STAND_ANGLES = [82, 77, 71, 107, 77, 94, 90, 88, 105, 134, 79, 113]

LEFT_LEG_FORWARD_STEP_ANGLES = [82, 77, 36, 84, 69, 80, 90, 88, 105, 134, 94, 105]

ONE_DEGREE_ANGLES = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

joint_map = {
        "lhr": LHR_IDX, "lha": LHA_IDX, "lhe": LHE_IDX, "lkk": LK_IDX,
        "laa": LAA_IDX, "lae": LAE_IDX, "rhr": RHR_IDX, "rha": RHA_IDX,
        "rhe": RHE_IDX, "rkk": RK_IDX, "raa": RAA_IDX, "rae": RAE_IDX
    }