import tkinter as tk
from tkinter import ttk
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class PWM_Calibrate_Servos_GUI(tk.Frame):
    def __init__(self, width, height, parent_root):
        super().__init__(parent_root)

        self.width = width
        self.height = height

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.selected_button = "none"

        # Match Manual Control GUI structure
        self.leg_slider_angle_group = []
        self.leg_label_angle_group = []
        self.leg_text_angle_group = [
            "Left Hip Rotator: ", "Left Hip Aductor: ", "Left Hip Extendor: ",
            "Left Knee: ", "Left Ankle Aductor: ", "Left Ankle Extendor: ",
            "Right Hip Rotator: ", "Right Hip Aductor: ", "Right Hip Extendor: ",
            "Right Knee: ", "Right Ankle Aductor: ", "Right Ankle Extendor: "
        ]

        # Panels (same style)
        self.left_panel = tk.Frame(self)
        self.right_panel = tk.Frame(self)
        self.bottom_panel = tk.Frame(self)

        self.left_panel.grid(row=0, column=0, sticky="n", padx=20, pady=20)
        self.right_panel.grid(row=0, column=1, sticky="n", padx=20, pady=20)
        self.bottom_panel.grid(row=1, column=0, columnspan=2, sticky="n", pady=20)

        self.pwm_min_group = []
        self.pwm_max_group = []
        self.pwm_enabled_group = []

        # Load widgets (same pattern)
        self.load()

        # Initialize slider values (same pattern)
        self.new()

    # ----------------------------------------------------------
    # LOAD — identical purpose to Manual_Control_GUI.load()
    # ----------------------------------------------------------
    def load(self):
        for al in range(12):
            panel = self.left_panel if al < 6 else self.right_panel

            # Label
            lbl = tk.Label(
                panel,
                text="  " + self.leg_text_angle_group[al] + "0      ",
                width=35
            )
            lbl.grid(row=al % 6, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_label_angle_group.append(lbl)

            # Slider
            sld = ttk.Scale(
                panel,
                from_=0,
                to=180,
                orient="horizontal",
                command=lambda x, idx=al: self.get_slider_angle_value(idx)
            )
            sld.grid(row=al % 6, column=1, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_slider_angle_group.append(sld)

        # LEFT LEG (0–5)
        for i in range(6):
            row = i + 6  # place below the 6 sliders

            # Servo name
            tk.Label(
                self.left_panel,
                text=self.leg_text_angle_group[i] + " PWM: ",
                anchor="w",
                width=25
            ).grid(row=row, column=0, padx=10, pady=5)

            # Min PWM
            min_entry = tk.Entry(self.left_panel, width=8)
            min_entry.insert(0, "500")
            min_entry.grid(row=row, column=1, padx=5)
            self.pwm_min_group.append(min_entry)

            # Max PWM
            max_entry = tk.Entry(self.left_panel, width=8)
            max_entry.insert(0, "2500")
            max_entry.grid(row=row, column=2, padx=5)
            self.pwm_max_group.append(max_entry)

            # NEW: Checkbox for this servo
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(self.left_panel, variable=var)
            chk.grid(row=row, column=3, padx=10)
            self.pwm_enabled_group.append(var)

        # RIGHT LEG (6–11)
        for i in range(6, 12):
            row = (i - 6) + 6  # also below sliders

            # Servo name
            tk.Label(
                self.right_panel,
                text=self.leg_text_angle_group[i] + " PWM: ",
                anchor="w",
                width=25
            ).grid(row=row, column=0, padx=10, pady=5)

            # Min PWM
            min_entry = tk.Entry(self.right_panel, width=8)
            min_entry.insert(0, "500")
            min_entry.grid(row=row, column=1, padx=5)
            self.pwm_min_group.append(min_entry)

            # Max PWM
            max_entry = tk.Entry(self.right_panel, width=8)
            max_entry.insert(0, "2500")
            max_entry.grid(row=row, column=2, padx=5)
            self.pwm_max_group.append(max_entry)

            # NEW: Checkbox for this servo
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(self.right_panel, variable=var)
            chk.grid(row=row, column=3, padx=10)
            self.pwm_enabled_group.append(var)

        # Buttons (moved down below PWM grid)
        tk.Button(
            self.bottom_panel,
            text="Calibrate Servos",
            bg="green",
            fg="white",
            font=("Arial", 14),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.calibrate_button_click
        ).grid(row=20, column=0, padx=20, pady=20)

        tk.Button(
            self.bottom_panel,
            text="Exit",
            bg="green",
            fg="white",
            font=("Arial", 14),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.exit_button_click
        ).grid(row=20, column=1, padx=20, pady=20)

    # ----------------------------------------------------------
    # NEW — identical purpose to Manual_Control_GUI.new()
    # ----------------------------------------------------------
    def new(self):
        for al in range(12):
            self.leg_slider_angle_group[al].set(90)
            self.leg_label_angle_group[al].config(
                text="  " + self.leg_text_angle_group[al] + "90      "
            )

    # ----------------------------------------------------------
    # IDENTICAL TO Manual_Control_GUI.get_slider_angle_value()
    # ----------------------------------------------------------
    def get_slider_angle_value(self, leg):
        slider_val = self.leg_slider_angle_group[leg].get()
        rounded = round(slider_val)

        self.leg_label_angle_group[leg].config(
            text="  " + self.leg_text_angle_group[leg] + str(rounded) + "      "
        )

        return rounded

    def get_all_slider_angles(self):
        return [self.get_slider_angle_value(al) for al in range(12)]
    
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

    # ----------------------------------------------------------
    # UPDATE LOOP — same pattern
    # ----------------------------------------------------------
    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.selected_button == "pwm_calibrate":
            return False, "pwm_calibrate"

        if self.selected_button == "exit":
            return False, "exit"

        return True, "none"
