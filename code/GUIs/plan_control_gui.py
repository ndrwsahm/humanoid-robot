import os
import tkinter as tk
from tkinter import ttk
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Plan_Control_GUI(tk.Frame):
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

        self.load()
        self.new(starting_angles, starting_pos)

        self.mode = "Angles"
        self.position_number = 1

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

        # Run Custom Profile Button
        run_button = tk.Button(self, text="Run Custom Profile", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.run_custom_profile_button_click)
        run_button.place(x=100, y=400)

        # Exit Button
        exit_button = tk.Button(self, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=450, y=500)

        # Frame to hold the text box + button
        self.save_panel = tk.Frame(self)
        self.save_panel.place(x=900, y=20)   # adjust X/Y as needed

        # Text box with scrollbar
        self.save_scroll = tk.Scrollbar(self.save_panel)
        self.save_text = tk.Text(self.save_panel, width=30, height=30, yscrollcommand=self.save_scroll.set)
        self.save_scroll.config(command=self.save_text.yview)

        self.save_text.grid(row=0, column=0, padx=5, pady=5)
        self.save_scroll.grid(row=0, column=1, sticky="ns")

        # Save button
        self.save_button = tk.Button(self.save_panel, text="Save Position", bg="green", fg="white", font=("Arial", 12), width=20, command=self.save_current_position)
        self.save_button.grid(row=2, column=0, pady=10)

        self.file_name_entry = tk.Entry(self.save_panel, width=30)
        self.file_name_entry.grid(row=3, column=0, pady=10)   # adjust as needed

        self.save_file_button = tk.Button(self.save_panel, text="Save to File", bg="green", fg="white", font=("Arial", 12), width=20, command=self.save_to_file)
        self.save_file_button.grid(row=4, column=0, pady=10)

        self.clear_saved_positions_button = tk.Button(self.save_panel, text="Clear Saved Positions", bg="green", fg="white", font=("Arial", 12), width=20, command=self.clear_saved_positions)
        self.clear_saved_positions_button.grid(row=1, column=0, pady=10)

        # Single-line text box for selected profile
        self.selected_profile_entry = tk.Entry(self, width=30)
        self.selected_profile_entry.place(x=100, y=360)   # adjust as needed

        # Small text box showing files in custom_profiles folder
        self.profile_list_box = tk.Text(self, width=50, height=10)
        self.profile_list_box.place(x=400, y=320)  # adjust position as needed

        self.load_profile_list()

        self.profile_list_box.bind("<Double-1>", self.on_profile_double_click)

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
            "run_custom_profile": (True, "run_custom_profile"),
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

    def save_current_position(self):
        # Get angles
        angles = self.get_all_slider_angles()

        line = f"Position{self.position_number}: {angles}\n\n"
        self.position_number += 1

        # Insert into text box
        self.save_text.insert(tk.END, line)

        # Auto-scroll to bottom
        self.save_text.see(tk.END)

    def load_profile_list(self):
        folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "utilities",
            "custom_profiles"
        )

        print(f"Loading profiles from: {folder}")  # Debug statement

        # Clear box
        self.profile_list_box.delete("1.0", tk.END)

        # Ensure folder exists
        if not os.path.exists(folder):
            self.profile_list_box.insert(tk.END, "Profile folder not found.\n")
            return

        files = os.listdir(folder)

        if not files:
            self.profile_list_box.insert(tk.END, f"No profiles found at {folder}.\n")
            return

        self.profile_list_box.insert(tk.END, f"Profiles found at utilities\custom_profiles.\n\n\n")
        # List files
        for f in files:
            self.profile_list_box.insert(tk.END, f + "\n")

    def on_profile_double_click(self, event):
        # Get the clicked line index
        index = self.profile_list_box.index("@%s,%s linestart" % (event.x, event.y))
        line = self.profile_list_box.get(index, index + " lineend").strip()

        # Ignore empty lines
        if not line:
            return

        # Put filename into the entry box
        self.selected_profile_entry.delete(0, tk.END)
        self.selected_profile_entry.insert(0, line)

    def save_to_file(self):
        # Get filename from entry box
        filename = self.file_name_entry.get().strip()

        if not filename:
            print("No filename entered.")
            return

        # Ensure .ini extension
        if not filename.endswith(".ini"):
            filename += "_" + str(ID) + ".ini"

        # Build full path to custom_profiles folder
        folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "utilities",
            "custom_profiles"
        )

        # Ensure folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        full_path = os.path.join(folder, filename)

        # Get all saved positions from the text box
        content = self.save_text.get("1.0", tk.END).strip()

        # Write to file
        with open(full_path, "w") as f:
            f.write(content)

        print(f"Saved profile to: {full_path}")

    def clear_saved_positions(self):
        self.save_text.delete("1.0", tk.END)
        self.position_number = 1  

    def get_selected_profile_path(self):
        # Get raw filename from the text box
        filename = self.selected_profile_entry.get().strip()

        if not filename:
            print("No profile selected.")
            return None
        return filename
    
    def get_movement_click(self, movement): self.selected_button = movement
    def get_mode(self): return self.mode
    def stand_button_click(self): self.selected_button = "stand"
    def run_custom_profile_button_click(self): self.selected_button = "run_custom_profile"
    #def save_to_file(self): self.selected_button = "save_to_file"
    def exit_button_click(self): self.selected_button = "exit"; self.close()
    def close(self): self.destroy()
    
   
