import os
import tkinter as tk
from tkinter import ttk
from globals import *

from GUIs.utilities.utils import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Plan_Control_GUI(tk.Frame):
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

        # Panels
        self.save_panel = tk.Frame(self)
        self.bottom_panel = tk.Frame(self)

        self.save_panel.place(x=800, y=20)  # Adjust as needed
        self.bottom_panel.place(x=10, y=450)
        
        # Load servo sliders
        self.head_panel, self.left_arm_panel, self.right_arm_panel, self.left_leg_panel, self.right_leg_panel = create_servo_sliders(self)
        self.left_arm_pos_panel, self.right_arm_pos_panel, self.left_leg_pos_panel, self.right_leg_pos_panel = create_pos_sliders(self)

        self.load_buttons()
        self.new(starting_angles, starting_pos)

        self.mode = "Angles"
        self.position_number = 1
        self.initialized = True

    def load_buttons(self):
        # Bottom Panel Buttons
        #####################################
        mode_button = tk.Button(self.bottom_panel, text="Mode", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: mode_button_click(self))
        mode_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Run Custom Profile Button
        run_button = tk.Button(self.bottom_panel, text="Run Custom Profile", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.run_custom_profile_button_click)
        run_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Exit Button
        exit_button = tk.Button(self.bottom_panel, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Single-line text box for selected profile
        self.selected_profile_entry = tk.Entry(self.bottom_panel, width=30)
        self.selected_profile_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # adjust as needed

        # Small text box showing files in custom_profiles folder
        self.profile_list_box = tk.Text(self.bottom_panel, width=50, height=10)
        self.profile_list_box.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky="w")  # adjust position as needed
        self.profile_list_box.config(state="normal")
        self.profile_list_box.bind("<Double-1>", self.on_profile_double_click)
        self.profile_list_box.bind("<Double-Button-1>", self.on_profile_double_click)
        self.profile_list_box.bind("<Button-1>", self.on_profile_double_click)

        self.load_profile_list()

        # Save Panel Buttons and Text Box
        #####################################
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
      
    def new(self, angles, pos):
        self.head_panel.set_all([90,90])
        self.left_arm_panel.set_all([90,90,90])
        self.right_arm_panel.set_all([90,90,90])
        self.left_leg_panel.set_all(angles[0:6])
        self.right_leg_panel.set_all(angles[6:12])
        #self.left_arm_pos_panel.set_all(pos[0:3])
        #self.right_arm_pos_panel.set_all(pos[0:3])
        self.left_leg_pos_panel.set_all(pos[0:3])
        self.right_leg_pos_panel.set_all(pos[0:3])

    def gui_update(self):
        self.update_idletasks()
        self.update()

        self.load_profile_list()

        if self.mode != getattr(self, "last_mode", None):
            if self.mode == "Kinematics":
                hide_angle_sliders(self)
                show_kinematic_sliders(self)
            elif self.mode == "Angles":
                hide_kinematic_sliders(self)
                show_angle_sliders(self)
            self.last_mode = self.mode

        button_actions = {
            "run_custom_profile": (True, "run_custom_profile"),
            "exit": (False, self.selected_button)
        }

        result = button_actions.get(self.selected_button, (True, "none"))
        self.selected_button = "none" # Reset after handling
        return result
   
    def save_current_position(self):
        # Get angles
        angles = get_all_slider_angles(self)

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
        print("Clicked line:")

        # Get the index of the clicked position
        index = self.profile_list_box.index(f"@{event.x},{event.y}")

        # Get the full line number
        line_number = index.split(".")[0]

        # Extract the entire line
        line = self.profile_list_box.get(f"{line_number}.0", f"{line_number}.end").strip()

        # Ignore empty or header lines
        if not line or "Profiles found" in line:
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
    
   
