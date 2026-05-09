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

class Calibrate_Servos_GUI(tk.Frame):
    def __init__(self, width, height, parent_root):
        super().__init__(parent_root)

        self.width = width
        self.height = height

        center_window(parent_root, self.width, self.height)

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.selected_button = "none"

        # Load servo sliders
        self.head_panel, self.left_arm_panel, self.right_arm_panel, self.left_leg_panel, self.right_leg_panel = create_servo_sliders(self)

        row = 4
        self.bottom_panel = tk.Frame(self)
        self.bottom_panel.grid(row=row, column=0, columnspan=2, sticky="n", pady=BETWEEN_FRAME_YPADDING)

        # Load widgets 
        self.load_buttons()

        # Initialize slider values 
        self.new()

    # ----------------------------------------------------------
    # LOAD 
    # ----------------------------------------------------------
    def load_buttons(self):
        # Instructions
        instructions = (
            "Calibration Instructions:\n\n"
            "1. Adjust each servo slider until the PHYSICAL robot joint\n"
            "   is as close to 90° as possible.\n\n"
            "2. Ensure both legs look symmetrical and stable.\n\n"
            "3. When satisfied, press 'Calibrate Servos' to save offsets."
        )

        row = 0
        self.instruction_label = tk.Label(self.bottom_panel,text=instructions,justify="left",font=("Arial", 9),wraplength=350)
        self.instruction_label.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        # Buttons
        self.calibrate_servo_button = tk.Button(self.bottom_panel,text="Calibrate Servos",bg="green",fg="white",font=("Arial", 14),width=BUTTON_WIDTH,height=BUTTON_HEIGHT,command=self.calibrate_button_click )
        self.calibrate_servo_button.grid(row=row, column=0, padx=20, pady=20)
        row += 1

        self.exit_button = tk.Button(self.bottom_panel, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        self.exit_button.grid(row=row, column=1, padx=20, pady=20)

    def new(self):
        self.head_panel.reset_all()
        self.left_arm_panel.reset_all()
        self.right_arm_panel.reset_all()
        self.left_leg_panel.reset_all()
        self.right_leg_panel.reset_all()

    # BUTTON CALLBACKS
    # ----------------------------------------------------------
    def calibrate_button_click(self):
        self.selected_button = "calibrate"

    def exit_button_click(self):
        self.selected_button = "exit"
        self.destroy()

    # ----------------------------------------------------------
    # UPDATE LOOP 
    # ----------------------------------------------------------
    def gui_update(self):
        self.update_idletasks()
        self.update()

        if self.selected_button == "calibrate":
            return False, "calibrate"

        if self.selected_button == "exit":
            return False, "exit"

        return True, "none"
