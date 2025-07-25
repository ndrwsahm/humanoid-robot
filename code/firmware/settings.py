A1_LENGTH = 5   # cm
A2_LENGTH = 7   # cm
A3_LENGTH = 11  # cm 

LEFT_LEG_PINS = (3, 4, 5, 9, 10, 11)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor
RIGHT_LEG_PINS = (0, 1, 2, 12, 13, 14)    # hip rotator, hip aductor, hip extendor, knee, ankle aductor, ankle extendor

PULSE_WIDTH_MIN = 0
PULSE_WIDTH_MAX = 1
PULSE_WIDTH_SETTINGS = ((500, 2500), (500, 2500), (500, 2500),  # pins (0, 1, 2)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (3, 4, 5)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (6, 7, 8)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (9, 10, 11)
                        (500, 2500), (500, 2500), (500, 2500),  # pins (12, 13, 14)
                        (500, 2500), (500, 2500), (500, 2500))  # pins (15, 16)
