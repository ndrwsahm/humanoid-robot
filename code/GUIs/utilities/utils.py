from GUIs.utilities.servo_sliders import ServoSliderGroup
from GUIs.utilities.utility_sliders import LabeledSliderGroup
from globals import *

def center_window(window, width, height):
    window.update_idletasks()  # ensures correct geometry

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - 30

    window.geometry(f"{width}x{height}+{x}+{y}")

def create_servo_sliders(panel):
    # Text Labels
    head_text_angle_group = ["Head Yaw: ", "Head Roll: "]

    left_arm_text_angle_group = ["Left Shoulder Rotator: ", "Left Shoulder Aductor: ", "Left Elbow: "]
    right_arm_text_angle_group = ["Right Shoulder Rotator: ", "Right Shoulder Aductor: ", "Right Elbow: "]

    left_leg_text_angle_group = [
        "Left Hip Rotator: ", "Left Hip Aductor: ", "Left Hip Extendor: ",
        "Left Knee: ", "Left Ankle Aductor: ", "Left Ankle Extendor: "
    ]
    right_leg_text_angle_group = [
        "Right Hip Rotator: ", "Right Hip Aductor: ", "Right Hip Extendor: ",
        "Right Knee: ", "Right Ankle Aductor: ", "Right Ankle Extendor: "
    ]

    # Slider Creation
    row = 0
    head_panel = ServoSliderGroup(panel,head_text_angle_group,rows=2)
    head_panel.grid(row=row, column=0, columnspan=2, pady=10)
    row += 1

    left_arm_panel = ServoSliderGroup(panel,left_arm_text_angle_group,rows=3)
    left_arm_panel.grid(row=row, column=0, pady=10)

    right_arm_panel = ServoSliderGroup(panel,right_arm_text_angle_group,rows=3)
    right_arm_panel.grid(row=row, column=1, pady=10)
    row += 1

    left_leg_panel = ServoSliderGroup(panel,left_leg_text_angle_group,rows=6)
    left_leg_panel.grid(row=row, column=0, pady=10)

    right_leg_panel = ServoSliderGroup(panel,right_leg_text_angle_group,rows=6)
    right_leg_panel.grid(row=row, column=1, pady=10)
    row += 1

    return head_panel, left_arm_panel, right_arm_panel, left_leg_panel, right_leg_panel

def create_pos_sliders(panel):
    left_arm_text_angle_group = ["Left Hand X Position: ", "Left Hand Y Position: ", "Left Hand Z Position: "]
    right_arm_text_angle_group = ["Right Hand X Position: ", "Right Hand Y Position: ", "Right Hand Z Position: "]

    left_arm_pos_panel = ServoSliderGroup(panel, left_arm_text_angle_group, rows=3)
    left_arm_pos_panel.grid(row=0, column=0, pady=10)
    right_arm_pos_panel = ServoSliderGroup(panel, right_arm_text_angle_group, rows=3)
    right_arm_pos_panel.grid(row=0, column=1, pady=10)

    names = ["Left Foot X Position:  ", "Left Foot Y Position: ", "Left Foot Z Position: "]
    mins = [FOOT_X_MIN, FOOT_Y_MIN, FOOT_Z_MIN]
    maxs = [FOOT_X_MAX, FOOT_Y_MAX, FOOT_Z_MAX]
    orients = ["horizontal", "horizontal", "horizontal"]
    defaults = [0, 0, WALKING_HEIGHT]
    commands = [lambda val: get_slider_pos_value(panel, LEFT_FOOT_X), lambda val: get_slider_pos_value(panel, LEFT_FOOT_Y), lambda val: get_slider_pos_value(panel, LEFT_FOOT_Z)]

    left_leg_pos_panel = LabeledSliderGroup(panel, names, mins, maxs, orients, defaults, commands, rows=3)
    left_leg_pos_panel.grid(row=0, column=0, pady=10)
    right_leg_pos_panel = LabeledSliderGroup(panel, names, mins, maxs, orients, defaults, commands, rows=3)
    right_leg_pos_panel.grid(row=0, column=1, pady=10)

    return left_arm_pos_panel, right_arm_pos_panel, left_leg_pos_panel, right_leg_pos_panel

def create_utility_sliders(panel, speed, step_length, num_steps, commands):
    names=["Shift Forward: ","Shift Weight: ","Shift Height: ","Speed: ",
            "Step Length: ","Number of Steps: "]

    mins = [SHIFT_FORWARD_MIN, SHIFT_WEIGTH_MIN, SHIFT_HEIGTH_MIN, 10, 0.5, 1]
    maxs = [SHIFT_FORWARD_MAX, SHIFT_WEIGTH_MAX, SHIFT_HEIGTH_MAX, 100, 2, 10]
    orients = ["horizontal", "horizontal", "vertical", "horizontal", "horizontal", "horizontal"]
    defaults = [FOOT_X_CENTER, 0, WALKING_HEIGHT, speed, step_length, num_steps]

    walking_params = LabeledSliderGroup(panel, names, mins, maxs, orients, defaults, commands, rows=6, label_width=20)
    walking_params.grid(row=0, column=0, sticky="nsew")
    return walking_params

################################################
# Getters
################################################
# Angles Sliders
def get_slider_angle_value(gui, leg):
    slider_val = 0
    slider_val = gui.left_leg_panel.sliders[leg].get() if leg < 6 else gui.right_leg_panel.sliders[leg-6].get()

    return round(slider_val)

def get_arm_slider_angle_value(gui, arm):
    slider_val = 0
    slider_val = gui.left_arm_panel.sliders[arm].get() if arm < 3 else gui.right_arm_panel.sliders[arm-3].get()

    return round(slider_val)

def get_head_slider_angle_value(gui, head):
    slider_val = 0
    slider_val = gui.head_panel.sliders[head].get()

    return round(slider_val)

def get_all_slider_angles(gui):
        return [get_slider_angle_value(gui, al) for al in range(12)]

def get_all_slider_arm_angles(gui):
    return [get_arm_slider_angle_value(gui, al) for al in range(6)]

def get_all_slider_head_angles(gui):
    return [get_head_slider_angle_value(gui, al) for al in range(2)]

# Position Sliders
def get_slider_pos_value(gui, leg):
    slider_val = 0
    try:
        slider_val = gui.left_leg_pos_panel.sliders[leg].get() if leg < 3 else gui.right_leg_pos_panel.sliders[leg-3].get()
    except Exception as e:
        print("Error getting slider al position: " + str(e))
    return round(slider_val)

def get_all_slider_pos(gui):
    all_angles = []
    for al in ALL_POS:
        all_angles.append(get_slider_pos_value(gui,al))

    return all_angles

# Utility Sliders  
def get_slider_forward_val(gui, val):
    if not gui.initialized:
        return
    
    # Apply shift (example logic: add shift_val to left, subtract from right)
    gui.left_leg_pos_panel.sliders[0].set(val)
    gui.right_leg_pos_panel.sliders[0].set(val)

    gui.left_leg_pos_panel._update_label(0, val)
    gui.right_leg_pos_panel._update_label(0, val)

    return float(val)

def get_slider_weight_val(gui, val):
        if not gui.initialized:
            return
        
        # Apply shift (example logic: add shift_val to left, subtract from right)
        gui.left_leg_pos_panel.sliders[1].set(val)
        gui.right_leg_pos_panel.sliders[1].set(val)

        gui.left_leg_pos_panel._update_label(1, val)
        gui.right_leg_pos_panel._update_label(1, val)

        return float(val)

def get_slider_height_val(gui, val):
    if not gui.initialized:
        return

    # Apply shift (example logic: add shift_val to left, subtract from right)
    gui.left_leg_pos_panel.sliders[2].set(val)
    gui.right_leg_pos_panel.sliders[2].set(val)

    gui.left_leg_pos_panel._update_label(2, val)
    gui.right_leg_pos_panel._update_label(2, val)
    return float(val)

#######################################
# Setters
#######################################
# Angles Sliders
def set_all_slider_angles(gui, angles):
    if not gui.initialized:
        return
    
    for al in ALL_LEGS:
        gui.left_leg_panel.sliders[al].set(angles[al]) if al < 6 else gui.right_leg_panel.sliders[al-6].set(angles[al])

def set_all_slider_arm_angles(gui, angles):
    if not gui.initialized:
        return
    
    for al in ALL_ARMS:
        gui.left_arm_panel.sliders[al].set(angles[al]) if al < 3 else gui.right_arm_panel.sliders[al-3].set(angles[al])

def set_all_slider_head_angles(gui, angles):
    if not gui.initialized:
        return
    
    for al in ALL_HEAD:
        gui.head_panel.sliders[al].set(angles[al])

# Position Sliders
def set_all_slider_pos(gui, pos):
    if not gui.initialized:
        return
    
    try:
        for al in ALL_POS:
            gui.left_leg_pos_panel.sliders[al].set(pos[al]) if al < 3 else gui.right_leg_pos_panel.sliders[al-3].set(pos[al])
    except Exception as e:
        print("Error setting slider positions: " + str(e))

# Utility Sliders
def set_speed_val(gui, val):
    val = int(float(val))
    gui.speed = val
    try:
        gui.walking_params._update_label(2, val)  # Update Speed label in LabeledSliderGroup
    except:
        pass
    return val

def set_step_length_val(gui, val):
    val = round(float(val) * 2) / 2.0
    gui.step_length = val
    try:
        gui.walking_params._update_label(3, val)  # Update Step Length label in LabeledSliderGroup
    except:
        pass
    return val

def set_num_steps_val(gui, val):
    val = int(float(val))
    gui.num_steps = val
    try:
        gui.walking_params._update_label(4, val)  # Update Number of Steps label in LabeledSliderGroup
    except:
        pass
    return val

######################################
# GUI-SPECIFIC FUNCTIONS
######################################
def mode_button_click(gui):
    if gui.mode == "Kinematics":
        gui.mode = "Angles"

    elif gui.mode == "Angles":
        gui.mode = "Kinematics"

    gui.selected_button = "mode"

def show_angle_sliders(gui):
    gui.head_panel.show()
    gui.left_arm_panel.show()
    gui.right_arm_panel.show()
    gui.left_leg_panel.show()
    gui.right_leg_panel.show()

def hide_angle_sliders(gui):
    gui.head_panel.hide()
    gui.left_arm_panel.hide()
    gui.right_arm_panel.hide()
    gui.left_leg_panel.hide()
    gui.right_leg_panel.hide()

def show_kinematic_sliders(gui):
    gui.left_arm_pos_panel.show()
    gui.right_arm_pos_panel.show()
    gui.left_leg_pos_panel.show()
    gui.right_leg_pos_panel.show()      

def hide_kinematic_sliders(gui):
    gui.left_arm_pos_panel.hide()
    gui.right_arm_pos_panel.hide()
    gui.left_leg_pos_panel.hide()
    gui.right_leg_pos_panel.hide()


    
