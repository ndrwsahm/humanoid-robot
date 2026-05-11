import tkinter as tk
from tkinter import ttk
from globals import *

from GUIs.utilities.utils import *

COLUMN_WIDTH_PADDING = 10
ROW_HEIGHT_PADDING = 3
BETWEEN_FRAME_XPADDING = 10
BETWEEN_FRAME_YPADDING = 2

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Manual_Control_GUI(tk.Frame):
    def __init__(self, width, height, starting_angles, starting_pos, parent_root):
        super().__init__(parent_root) 

        # Screen Dimensions
        self.width = width
        self.height = height

        center_window(parent_root, self.width, self.height)

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False) 

        self.selected_button = "none"
        self.initialized = False

        self.speed = DEFAULT_SPEED  # default mid-speed
        self.step_length = 1  # default mid-step length
        self.num_steps = 4 # default 1 step

        # Panels 
        self.left_bottom_panel = tk.Frame(self)
        self.right_bottom_panel = tk.Frame(self)

        self.grid_rowconfigure(3, weight=1)
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        starting_row = 0
 
        self.left_bottom_panel.grid(row=starting_row + 3, column=0, sticky="s", pady=BETWEEN_FRAME_YPADDING)
        self.right_bottom_panel.grid(row=starting_row + 3, column=1, sticky="s", pady=BETWEEN_FRAME_YPADDING)        

        self.movement_group = []
        self.movements = ["stand", "walk_forward", "walk_backward", "turn_right", "turn_left"]
        self.movement_labels = ["Stand", "Walk Forward", "Walk Backward", "Turn Right", "Turn Left"]

        self.movement_positions = [
            (0, 1), (2, 1), (2, 2),
            (1, 1), (3, 1)
        ]

        # Load servo sliders
        self.head_panel, self.left_arm_panel, self.right_arm_panel, self.left_leg_panel, self.right_leg_panel = create_servo_sliders(self)
        commands = [lambda val: get_slider_forward_val(self, val), lambda val: get_slider_weight_val(self, val), lambda val: get_slider_height_val(self, val), lambda val: set_speed_val(self, val), lambda val: set_step_length_val(self, val), lambda val: set_num_steps_val(self, val)]
        self.walking_params = create_utility_sliders(self.left_bottom_panel, self.speed, self.step_length, self.num_steps, commands)

        self.left_arm_pos_panel, self.right_arm_pos_panel, self.left_leg_pos_panel, self.right_leg_pos_panel = create_pos_sliders(self)

        self.load_buttons()
        self.new(starting_angles, starting_pos)

        self.mode = "Angles"
        self.initialized = True

    def load_buttons(self):
        # Mode button
        mode_button = tk.Button(self.right_bottom_panel, text="Mode", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: mode_button_click(self))
        mode_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Movement buttons
        for k in range(len(self.movements)):
            # TODO create second row automatically
            self.movement_group.append(tk.Button(self.right_bottom_panel, text=self.movement_labels[k], bg="green", fg="white", font=("Arial", 10), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda m=self.movements[k]: self.get_movement_click(m)))

        for k, (x, y) in enumerate(self.movement_positions):
            self.movement_group[k].grid(row=y, column=x, padx=5, pady=5, sticky="w")

        # Exit Button
        exit_button = tk.Button(self.right_bottom_panel, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.grid(row=8, column=0, pady=20)
 
    def new(self, angles, pos):
        self.head_panel.set_all([90,90])
        self.left_arm_panel.set_all([90,90,90])
        self.right_arm_panel.set_all([90,90,90])
        self.left_leg_panel.set_all(angles[0:6])
        self.right_leg_panel.set_all(angles[6:12])
        #self.left_arm_pos_panel.set_all(pos[0:3])
        #self.right_arm_pos_panel.set_all(pos[0:3])
        self.left_leg_pos_panel.set_all(pos[0:3])
        self.right_leg_pos_panel.set_all(pos[3:6])

    def hide_walk_buttons(self):
        for k in range(len(self.movements)):
            self.movement_group[k].grid_forget()

    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.mode != getattr(self, "last_mode", None):
            if self.mode == "Kinematics":
                hide_angle_sliders(self)
                show_kinematic_sliders(self)
            elif self.mode == "Angles":
                hide_kinematic_sliders(self)
                show_angle_sliders(self)
            self.last_mode = self.mode

        button_actions = {
            "stand": (True, "stand"),
            "walk_forward": (True, "walk_forward"),
            "walk_backward": (True, "walk_backward"),
            "turn_left": (True, "turn_left"),
            "turn_right": (True, "turn_right"),
            "exit": (False, self.selected_button)
        }

        result = button_actions.get(self.selected_button, (True, "none"))
        self.selected_button = "none" # Reset after handling
        return result

    # ----------------------------------------------------------
    # UTILITY FUNCTIONS — specific to this GUI only
    # ---------------------------------------------------------- 
    def get_frames(self):
        # Speed 1 → 60 frames (slow)
        # Speed 100 → 5 frames (fast)
        min_frames = 5
        max_frames = 60
        return int(max_frames - (self.speed / 100) * (max_frames - min_frames))

    def get_speed(self): return self.speed
    def get_step_length(self): return self.step_length
    def get_num_steps(self): return self.num_steps
    
    def get_movement_click(self, movement): self.selected_button = movement
    def get_mode(self): return self.mode
    def stand_button_click(self): self.selected_button = "stand"
    def exit_button_click(self): self.selected_button = "exit"; self.close()
    def close(self): self.destroy()
    
   
