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

        self.initialized = False
        self.no_pos_sliders = True

        self.width = width
        self.height = height

        center_window(parent_root, self.width, self.height)

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.selected_button = "none"

        self.checkbox_top_panel = tk.Frame(self)
        self.checkbox_top_panel.grid(row=0, column=2, sticky="nw", pady=10)

        # Load servo sliders
        self.head_panel, self.left_arm_panel, self.right_arm_panel, self.left_leg_panel, self.right_leg_panel = create_servo_sliders(self)
                           
        self.checkbox_top_left_panel = tk.Frame(self)
        self.checkbox_top_left_panel.grid(row=1, column=2, sticky="nw", pady=10)

        self.checkbox_top_right_panel = tk.Frame(self)
        self.checkbox_top_right_panel.grid(row=1, column=2, sticky="n", pady=10)

        self.checkbox_bottom_left_panel = tk.Frame(self)
        self.checkbox_bottom_left_panel.grid(row=2, column=2, sticky="nw", pady=10)

        self.checkbox_bottom_right_panel = tk.Frame(self)
        self.checkbox_bottom_right_panel.grid(row=2, column=2, sticky="n", pady=10)

        row = 4
        self.bottom_panel = tk.Frame(self)
        self.bottom_panel.grid(row=row, column=0, columnspan=2, sticky="n", pady=BETWEEN_FRAME_YPADDING)

        self.right_panel = tk.Frame(self, bg="lightgrey")

        self.right_panel.grid(row=4, column=2, sticky="n")
        self.right_panel.config(width=400, height=200)
        
        # Load widgets 
        self.load_buttons()

        self.status_bar = create_status_bar(self.right_panel, 15, 80, 10)
        self.status_bar.grid(row=0, column=0, sticky="nsew")

        # Initialize slider values 
        self.new()

        self.mode = "Angles"
        self.initialized = True

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
        self.calibrate_servo_button.grid(row=row, column=0, padx=20, pady=10)
        row += 1

        self.exit_button = tk.Button(self.bottom_panel, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        self.exit_button.grid(row=row, column=1, padx=20, pady=10)

        if DRAW_DEBUG_BOXES:
            debug_box(self.head_panel, "blue")
            debug_box(self.left_arm_panel, "green")
            debug_box(self.right_arm_panel, "purple")
            debug_box(self.left_leg_panel, "orange")
            debug_box(self.right_leg_panel, "brown")

            debug_box(self.checkbox_top_left_panel, "red")
            debug_box(self.bottom_panel, "black")
            debug_box(self.right_panel, "yellow")

        self.calibrate_checkbox = []
        for k in range(NUMBER_OF_ALL_SERVOS):
            row = k + 1
            # Checkbox for this servo
            if row < 3:
                panel = self.checkbox_top_panel
            elif row < 6:
                panel = self.checkbox_top_left_panel
                row = row - 1
            elif row < 9:
                panel = self.checkbox_top_right_panel
                row = row - 5
            elif row < 15:
                panel = self.checkbox_bottom_left_panel
                row = row - 8
            else:
                panel = self.checkbox_bottom_right_panel

            lbl = tk.Label(panel,text=f"{ALL_BODY_FULL_NAMES[k]} ",anchor="w")
            lbl.grid(row=row, column=0)

            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(panel, variable=var, pady=5)
            chk.grid(row=row, column=1)
            self.calibrate_checkbox.append(var)

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
    
    def get_mode(self): return self.mode
