A1_LENGTH = 5   # cm
A2_LENGTH = 7   # cm
A3_LENGTH = 11  # cm 

LEFT_LEG_PINS = (8, 9, 10, 11, 12, 13)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
RIGHT_LEG_PINS = (0, 1, 2, 3, 4, 5)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

# Phils pins
#LEFT_LEG_PINS = (10, 11, 12, 13, 14, 15)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
#RIGHT_LEG_PINS = (0, 1, 2, 3, 4, 5)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor


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

STANDING_ANGLES = [82, 88, 71, 73, 77, 94, 90, 96, 105, 134, 103, 121]

LEFT_LEAN_ANGLES = [82, 105, 71, 73, 88, 94, 90, 96, 105, 134, 103, 121]

LEFT_LEG_STAND_ANGLES = [82, 88, 71, 73, 92, 94, 84, 100, 105, 100, 103, 121]

RIGHT_LEAN_ANGLES = [82, 88, 71, 73, 77, 94, 90, 77, 105, 134, 94, 121]

RIGHT_LEG_STAND_ANGLES = [82, 77, 71, 107, 77, 94, 90, 88, 105, 134, 80, 113]

ONE_DEGREE_ANGLES = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]