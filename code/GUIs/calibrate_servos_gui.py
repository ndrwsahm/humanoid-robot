import tkinter as tk
from tkinter import ttk
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Calibrate_Servos_GUI(tk.Frame):
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

        # Instructions
        instructions = (
            "Calibration Instructions:\n\n"
            "1. Adjust each servo slider until the PHYSICAL robot joint\n"
            "   is as close to 90° as possible.\n\n"
            "2. Ensure both legs look symmetrical and stable.\n\n"
            "3. When satisfied, press 'Calibrate Servos' to save offsets."
        )

        tk.Label(
            self.bottom_panel,
            text=instructions,
            justify="left",
            font=("Arial", 12),
            wraplength=600
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons
        tk.Button(
            self.bottom_panel,
            text="Calibrate Servos",
            bg="green",
            fg="white",
            font=("Arial", 14),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.calibrate_button_click
        ).grid(row=1, column=0, padx=20, pady=20)

        tk.Button(
            self.bottom_panel,
            text="Exit",
            bg="green",
            fg="white",
            font=("Arial", 14),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.exit_button_click
        ).grid(row=1, column=1, padx=20, pady=20)

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

    # ----------------------------------------------------------
    # BUTTON CALLBACKS
    # ----------------------------------------------------------
    def calibrate_button_click(self):
        self.selected_button = "calibrate"

    def exit_button_click(self):
        self.selected_button = "exit"
        self.destroy()

    # ----------------------------------------------------------
    # UPDATE LOOP — same pattern
    # ----------------------------------------------------------
    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.selected_button == "calibrate":
            return False, "calibrate"

        if self.selected_button == "exit":
            return False, "exit"

        return True, "none"
