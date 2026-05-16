import tkinter as tk
from tkinter import ttk
from globals import *
from GUIs.utilities.utils import *

COLUMN_WIDTH_PADDING = 10
ROW_HEIGHT_PADDING = 3
BETWEEN_FRAME_XPADDING = 10
BETWEEN_FRAME_YPADDING = 3

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class PWM_Calibrate_Servos_GUI(tk.Frame):
    def __init__(self, width, height, parent_root):
        super().__init__(parent_root)

        self.initialized = False
        self.no_pos_sliders = True
        
        self.width = width
        self.height = height

        center_window(parent_root, self.width, self.height)

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.selected_button = "none"

       # Load servo sliders
        self.head_panel, self.left_arm_panel, self.right_arm_panel, self.left_leg_panel, self.right_leg_panel = create_servo_sliders(self)

        row = 2
        self.left_bottom_panel = tk.Frame(self)
        self.left_bottom_panel.grid(row=row, column=2, columnspan=1, sticky="n", pady=BETWEEN_FRAME_YPADDING)
        self.right_bottom_panel = tk.Frame(self)
        self.right_bottom_panel.grid(row=row, column=3, columnspan=1, sticky="n", pady=BETWEEN_FRAME_YPADDING)
        
        row = 3
        self.bottom_panel = tk.Frame(self)
        self.bottom_panel.grid(row=row+1, column=0, columnspan=2, sticky="n", pady=BETWEEN_FRAME_YPADDING)

        row = 4
        # Status bar goes at the bottom of the entire window
        self.status_panel = tk.Frame(self)
        self.status_panel.grid(row=99, column=0, columnspan=4, sticky="nsew")

        # Allow the bottom row to expand
        self.grid_rowconfigure(99, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
                
        self.pwm_min_group = []
        self.pwm_max_group = []
        self.pwm_enabled_group = []

        # Load widgets
        self.load()
        
        self.status_bar = create_status_bar(self.status_panel, 10, 140, 10)
        self.status_bar.grid(row=0, column=0, sticky="nsew", padx=10)

        self.mode = "Angles"

        # Initialize slider values 
        self.new()

        self.initialized = True

    def load(self):
        
        for i in ALL_LEGS:
      
            if i < 6:
                panel = self.left_bottom_panel
                row = i + 6  

            else:
                panel = self.right_bottom_panel
                row = (i - 6) + 6 

            # Servo name
            lbl = tk.Label(panel,text=" PWM Limits: ",anchor="w",width=25)
            lbl.grid(row=row, column=0, padx=10, pady=5)

            # Min PWM
            min_entry = tk.Entry(panel, width=8)
            min_entry.insert(0, "500")
            min_entry.grid(row=row, column=1, padx=5)
            self.pwm_min_group.append(min_entry)

            # Max PWM
            max_entry = tk.Entry(panel, width=8)
            max_entry.insert(0, "2500")
            max_entry.grid(row=row, column=2, padx=5)
            self.pwm_max_group.append(max_entry)

            # Checkbox for this servo
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(panel, variable=var)
            chk.grid(row=row, column=3, padx=10)
            self.pwm_enabled_group.append(var)

        # Buttons 
        self.calibrate_button = tk.Button(self.bottom_panel, text="Calibrate Servos", bg="green", fg="white",font=("Arial", 14),width=BUTTON_WIDTH,height=BUTTON_HEIGHT, command=self.calibrate_button_click)
        self.calibrate_button.grid(row=20, column=0, padx=20, pady=20)
        
        self.exit_button = tk.Button( self.bottom_panel, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        self.exit_button.grid(row=20, column=1, padx=20, pady=20)

    def new(self):
        self.head_panel.reset_all()
        self.left_arm_panel.reset_all()
        self.right_arm_panel.reset_all()
        self.left_leg_panel.reset_all()
        self.right_leg_panel.reset_all()

    def get_pwm_min_max_values(self):
        pwm_min_settings = []
        pwm_max_settings = []
        for i in range(12):
            try:
                pwm_min = int(self.pwm_min_group[i].get())
                pwm_max = int(self.pwm_max_group[i].get())
            except ValueError:
                pwm_min, pwm_max = 500, 2500  # default values if parsing fails
            pwm_min_settings.append(pwm_min)
            pwm_max_settings.append(pwm_max)

        return pwm_min_settings, pwm_max_settings
    
    def get_all_pwm_settings(self):
        pwm_settings = []
        for i in range(12):
            try:
                pwm_min = int(self.pwm_min_group[i].get())
                pwm_max = int(self.pwm_max_group[i].get())
            except ValueError:
                pwm_min, pwm_max = 500, 2500  # default values if parsing fails
            pwm_settings.append((pwm_min, pwm_max)) 
        return pwm_settings

    def get_pwm_enabled_flags(self):
        return [var.get() for var in self.pwm_enabled_group]

    # ----------------------------------------------------------
    # BUTTON CALLBACKS
    # ----------------------------------------------------------
    def calibrate_button_click(self): 
        self.selected_button = "pwm_calibrate"

    def exit_button_click(self):
        self.selected_button = "exit"
        self.destroy()

    def get_mode(self): return self.mode
    # ----------------------------------------------------------
    # UPDATE LOOP 
    # ----------------------------------------------------------
    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.selected_button == "pwm_calibrate":
            return False, "pwm_calibrate"

        if self.selected_button == "exit":
            return False, "exit"

        return True, "none"
