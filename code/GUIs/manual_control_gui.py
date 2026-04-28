import tkinter as tk
from tkinter import ttk
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Manual_Control_GUI(tk.Frame):
    def __init__(self, width, height, starting_angles, starting_pos, parent_root):
        super().__init__(parent_root) 

        self.width = width
        self.height = height

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False) 

        self.selected_button = "none"

        self.leg_slider_angle_group = []
        self.leg_label_angle_group = []
        self.leg_text_angle_group = ["Left Hip Rotator: ", "Left Hip Aductor: ", "Left Hip Extendor: ", "Left Knee: ", "Left Ankle Aductor: ", "Left Ankle Extendor: ", "Right Hip Rotator: ", "Right Hip Aductor: ", "Right Hip Extendor: ", "Right Knee: ", "Right Ankle Aductor: ", "Right Ankle Extendor: "]
        
        self.leg_slider_pos_group = []
        self.leg_label_pos_group = []
        self.movement_group = []
        self.leg_text_pos_group = ["Left Foot X Position:  ", "Left Foot Y Position: ", "Left Foot Z Position: ", "Right Foot X Position: ", "Right Foot Y Position: ", "Right Foot Z Position: "]

        self.movements = ["stand", "walk_forward", "walk_backward", "turn_right", "turn_left"]
        self.movement_labels = ["Stand", "Walk Forward", "Walk Backward", "Turn Right", "Turn Left"]

        self.speed = DEFAULT_SPEED  # default mid-speed
        self.step_length = 1  # default mid-step length
        self.num_steps = 4 # default 1 step

        self.load()
        self.new(starting_angles, starting_pos)

        self.mode = "Angles"

    def load(self):
        # Anlge Track Sliders
        for al in ALL_LEGS:
            self.leg_slider_angle_group.append(ttk.Scale(self, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_angle_value(al)))
            self.leg_label_angle_group.append(tk.Label(self, text=self.leg_text_angle_group[al], width=35))

        self.empty_label = tk.Label(self, text = "")

        for al in ALL_POS:
            self.leg_slider_pos_group.append(ttk.Scale(self, from_=MIN_POS[al], to=MAX_POS[al], orient="horizontal", command=lambda x: self.get_slider_pos_value(al)))
            self.leg_label_pos_group.append(tk.Label(self, text=self.leg_text_pos_group[al], width=35))
        
        self.shift_weight_scale = ttk.Scale(self, from_=SHIFT_WEIGTH_MIN, to=SHIFT_WEIGTH_MAX, orient="horizontal", command=self.get_slider_weight_val)
        self.shift_weight_label = tk.Label(self, text="Shift Weight", width=35)
        self.shift_weight_scale.set(0)
        self.shift_height_scale = ttk.Scale(self, from_=SHIFT_HEIGTH_MAX, to=SHIFT_HEIGTH_MIN, orient="vertical", command=self.get_slider_height_val)
        self.shift_height_label = tk.Label(self, text="Shift Height", width=35)
        self.shift_height_scale.set(WALKING_HEIGHT)

        mode_button = tk.Button(self, text="Mode", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.mode_button_click)
        mode_button.place(x=150, y=500)

        x = 10
        y = 350
        offset = 0
                              #stand,   walk forward,                         walk backward,                        turn right,                     turn left
        movement_button_pos = [(x, y), (x + 2*(BUTTON_WIDTH + 200), y - 50), (x + 2*(BUTTON_WIDTH + 200), y + 50), (x + 3*(BUTTON_WIDTH + 200), y), (x + (BUTTON_WIDTH + 200), y)]
    
        for k in range(len(self.movements)):
            # TODO create second row automatically
            self.movement_group.append(tk.Button(self, text=self.movement_labels[k], bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda m=self.movements[k]: self.get_movement_click(m)))
            self.movement_group[k].place(x=movement_button_pos[k][0], y=movement_button_pos[k][1])
            #offset += BUTTON_WIDTH + 200

        # Speed Slider (User-facing)
        self.speed_scale = ttk.Scale(self,from_=10,to=100,orient="horizontal",command=self.get_speed_val)
        self.speed_scale.set(self.speed)
        self.speed_label = tk.Label(self, text=f"Speed: {self.speed}", width=35)

        # Place it (adjust x/y to match your layout)
        self.speed_label.place(x=625, y=420)
        self.speed_scale.place(x=700, y=450)

        # Step Length Slider (User-facing)
        self.step_length_scale = ttk.Scale(self,from_=0.5,to=2,orient="horizontal",command=self.get_step_length_val)
        self.step_length_scale.set(self.step_length)
        self.step_length_label = tk.Label(self, text=f"Step Length: {self.step_length}", width=35)

        # Place it (adjust x/y to match your layout)
        self.step_length_label.place(x=625, y=480)
        self.step_length_scale.place(x=700, y=510)

        # Number of Steps Slider (User-facing)
        self.num_steps_scale = ttk.Scale(self,from_=1,to=10,orient="horizontal",command=self.get_num_steps_val)
        self.num_steps_scale.set(self.num_steps)
        self.num_steps_label = tk.Label(self, text=f"Number of Steps: {self.num_steps}", width=35)

        # Place it (adjust x/y to match your layout)
        self.num_steps_label.place(x=625, y=540)
        self.num_steps_scale.place(x=700, y=570)

        # Exit Button
        exit_button = tk.Button(self, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=450, y=500)

    def new(self, angles, pos):
        for al in ALL_LEGS:
            self.leg_slider_angle_group[al].set(angles[al])

        for al in ALL_POS:
            self.leg_slider_pos_group[al].set(pos[al])

    def show_kinematic_sliders(self):
        for j in range(3): # number of servos per leg
            self.leg_slider_pos_group[j].grid(row=j, column=1, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_slider_pos_group[j+3].grid(row=j, column=4, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            
            self.leg_label_pos_group[j].grid(row=j, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_label_pos_group[j+3].grid(row=j, column=5, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

        self.empty_label = tk.Label(self, text="           ")
        self.empty_label.grid(row=3,column=3,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
   
        self.shift_weight_scale.grid(row=4,column=1,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.shift_weight_label.grid(row=4,column=2,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        
        self.shift_height_scale.grid(row=5,column=1,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.shift_height_label.grid(row=5,column=2,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

    def hide_kinematic_sliders(self):
        for al in ALL_POS:
            self.leg_slider_pos_group[al].grid_forget()
            self.leg_label_pos_group[al].grid_forget()
        
        self.shift_weight_scale.grid_forget()
        self.shift_weight_label.grid_forget()

        self.shift_height_scale.grid_forget()
        self.shift_height_label.grid_forget()
      
    def show_angle_sliders(self):
        for j in range(6): # number of servos per leg
            self.leg_slider_angle_group[j].grid(row=j, column=1, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_slider_angle_group[j+6].grid(row=j, column=4, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

            self.leg_label_angle_group[j].grid(row=j, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_label_angle_group[j+6].grid(row=j, column=5, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

        self.empty_label = tk.Label(self, text="           ")
        self.empty_label.grid(row=3,column=3,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

    def hide_angle_sliders(self):
        for al in ALL_LEGS:
            self.leg_slider_angle_group[al].grid_forget()
            self.leg_label_angle_group[al].grid_forget()

    def hide_walk_buttons(self):
        for k in range(len(self.movements)):
            self.movement_group[k].grid_forget()

    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.mode != getattr(self, "last_mode", None):
            if self.mode == "Kinematics":
                self.hide_angle_sliders()
                self.show_kinematic_sliders()
            elif self.mode == "Angles":
                self.hide_kinematic_sliders()
                self.show_angle_sliders()
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

    def get_slider_angle_value(self, leg):
        slider_val = 0
        slider_val = self.leg_slider_angle_group[leg].get()
        self.leg_label_angle_group[leg].config(text= "  " + self.leg_text_angle_group[leg] + str(round(slider_val, 2)) + "      ")
        
        return round(slider_val)
    
    def get_slider_pos_value(self, leg):
        slider_val = 0
        slider_val = self.leg_slider_pos_group[leg].get()
        self.leg_label_pos_group[leg].config(text=self.leg_text_pos_group[leg] + str(round(slider_val, 2)) + "      ")
        
        return round(slider_val)
    
    def get_slider_weight_val(self, val):
        # Apply shift (example logic: add shift_val to left, subtract from right)
        self.leg_slider_pos_group[LEFT_FOOT_Y].set(val)
        self.leg_slider_pos_group[RIGHT_FOOT_Y].set(val)

        # Update labels
        self.get_slider_pos_value(LEFT_FOOT_Y)
        self.get_slider_pos_value(RIGHT_FOOT_Y)
        return float(val)
    
    def get_slider_height_val(self, val):
        # Apply shift (example logic: add shift_val to left, subtract from right)
        self.leg_slider_pos_group[LEFT_FOOT_Z].set(val)
        self.leg_slider_pos_group[RIGHT_FOOT_Z].set(val)

        # Update labels
        self.get_slider_pos_value(LEFT_FOOT_Z)
        self.get_slider_pos_value(RIGHT_FOOT_Z)

        return float(val)
    
    def get_all_slider_angles(self):
        all_angles = []
        for al in ALL_LEGS:
            all_angles.append(self.get_slider_angle_value(al))
    
        return all_angles
    
    def set_all_slider_angles(self, angles):
        for al in ALL_LEGS:
            self.leg_slider_angle_group[al].set(angles[al])
    
    def get_all_slider_pos(self):
        all_angles = []
        for al in ALL_POS:
            all_angles.append(self.get_slider_pos_value(al))
    
        return all_angles
    
    def set_all_slider_pos(self, pos):
        for al in ALL_POS:
            self.leg_slider_pos_group[al].set(pos[al])
    
    def mode_button_click(self):
        if self.mode == "Kinematics":
            self.mode = "Angles"

        elif self.mode == "Angles":
            self.mode = "Kinematics"

        self.selected_button = "mode"

    def get_speed_val(self, val):
        val = int(float(val))
        self.speed = val
        try:
            self.speed_label.config(text=f"Speed: {val}")
        except:
            pass
        return val

    def get_speed(self):
        return self.speed

    def get_step_length_val(self, val):
        val = round(float(val) * 2) / 2.0
        self.step_length = val
        try:
            self.step_length_label.config(text=f"Step Length: {val}")
        except:
            pass
        return val

    def get_step_length(self):
        return self.step_length
    
    def get_num_steps_val(self, val):
        val = int(float(val))
        self.num_steps = val
        try:
            self.num_steps_label.config(text=f"Number of Steps: {val}")
        except:
            pass
        return val

    def get_num_steps(self):
        return self.num_steps
    
    def get_frames(self):
        # Speed 1 → 60 frames (slow)
        # Speed 100 → 5 frames (fast)
        min_frames = 5
        max_frames = 60
        return int(max_frames - (self.speed / 100) * (max_frames - min_frames))

    def get_movement_click(self, movement): self.selected_button = movement
    def get_mode(self): return self.mode
    def stand_button_click(self): self.selected_button = "stand"
    def exit_button_click(self): self.selected_button = "exit"; self.close()
    def close(self): self.destroy()
    
   
