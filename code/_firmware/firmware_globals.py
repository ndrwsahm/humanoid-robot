PI_COM_PORT = '/dev/ttyUSB0'
PI_BAUDRATE = 115200

PULSE_WIDTH_MIN = 0
PULSE_WIDTH_MAX = 1

# Leg Indexes
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

# Arm Indexes
LSR_IDX = 12
LSA_IDX = 13
LE_IDX = 14

RSR_IDX = 15
RSA_IDX = 16
RE_IDX = 17

# Head Indexes
HYA_IDX = 18
HRO_IDX = 19

HR_IDX = 0
HA_IDX = 1
HE_IDX = 2
KK_IDX = 3
AA_IDX = 4
AE_IDX = 5

ANGLES_TO_90 = [90, 90, 90, 90, 90, 90]
N90_DEGREE_START_ANGLES = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]

LOW_LIMIT = 0
HIGH_LIMIT = 1

ONE_DEGREE_ANGLES = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

joint_map = {
        "lhr": LHR_IDX, "lha": LHA_IDX, "lhe": LHE_IDX, "lkk": LK_IDX,
        "laa": LAA_IDX, "lae": LAE_IDX, "rhr": RHR_IDX, "rha": RHA_IDX,
        "rhe": RHE_IDX, "rkk": RK_IDX, "raa": RAA_IDX, "rae": RAE_IDX,
        "lsr": LSR_IDX, "lsa": LSA_IDX, "le": LE_IDX, "rsr": RSR_IDX,
        "rsa": RSA_IDX, "re": RE_IDX,
        "hya": HYA_IDX, "hro": HRO_IDX
    }