import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

from GUIs.utilities.utils import *

class HSV_Tuner_GUI(tk.Frame):
    def __init__(self, width, height, parent_root):
        super().__init__(parent_root)
        
        self.width = width
        self.height = height

        center_window(parent_root, self.width, self.height)
        parent_root.geometry(f"{self.width}x{self.height}")

        parent_root.resizable(True, False)   # width resizable, height fixed
        #self.config(width=self.width//2, height=self.height)

        self.pack_propagate(False)

        self.selected_button = "none"
        self.initialized = False

        self.left_panel = tk.Frame(self)
        self.right_panel = tk.Frame(self)
        self.bottom_panel = tk.Frame(self)

        self.left_panel.place(x=0, y=0, width=self.width//2, height=self.height//2)
        self.right_panel.place(x=self.width//2, y=0, width=self.width//2, height=self.height//2)
        self.bottom_panel.place(x=0, y=self.height//2, width=self.width, height=self.height//2)

        self.status_bar = create_status_bar(self.bottom_panel, 20, 40, 10)
        self.status_bar.grid(row=0, column=0, sticky="nsew")

        self.wall_hsv = []
        self.ball_hsv = []

        self.load_sliders()

    def load(self):
        # Base directory of this script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
  
    def load_sliders(self):
        wall_lbl = tk.Label(self.left_panel, text="Wall HSV")
        wall_lbl.place(x=20, y=20)

        # LEFT PANEL SLIDERS
        self.wall_h_min = tk.Scale(self.left_panel, from_=0, to=179, orient="horizontal",
                            label="H Min", command=self.on_slider_change)
        self.wall_s_min = tk.Scale(self.left_panel, from_=0, to=255, orient="horizontal",
                            label="S Min", command=self.on_slider_change)
        self.wall_v_min = tk.Scale(self.left_panel, from_=0, to=255, orient="horizontal",
                            label="V Min", command=self.on_slider_change)

        self.wall_h_min.place(x=20, y=20+20, width=100)
        self.wall_s_min.place(x=20, y=90+20, width=100)
        self.wall_v_min.place(x=20, y=160+20, width=100)

        # RIGHT PANEL SLIDERS
        self.wall_h_max = tk.Scale(self.left_panel, from_=0, to=179, orient="horizontal",
                            label="H Max", command=self.on_slider_change)
        self.wall_s_max = tk.Scale(self.left_panel, from_=0, to=255, orient="horizontal",
                            label="S Max", command=self.on_slider_change)
        self.wall_v_max = tk.Scale(self.left_panel, from_=0, to=255, orient="horizontal",
                            label="V Max", command=self.on_slider_change)

        self.wall_h_max.place(x=20+100, y=20+20, width=100)
        self.wall_s_max.place(x=20+100, y=90+20, width=100)
        self.wall_v_max.place(x=20+100, y=160+20, width=100)

        ball_lbl = tk.Label(self.right_panel, text="Bll HSV")
        ball_lbl.place(x=20, y=20)

        # LEFT PANEL SLIDERS
        self.ball_h_min = tk.Scale(self.right_panel, from_=0, to=179, orient="horizontal",
                            label="H Min", command=self.on_slider_change)
        self.ball_s_min = tk.Scale(self.right_panel, from_=0, to=255, orient="horizontal",
                            label="S Min", command=self.on_slider_change)
        self.ball_v_min = tk.Scale(self.right_panel, from_=0, to=255, orient="horizontal",
                            label="V Min", command=self.on_slider_change)

        self.ball_h_min.place(x=20, y=20+20, width=100)
        self.ball_s_min.place(x=20, y=90+20, width=100)
        self.ball_v_min.place(x=20, y=160+20, width=100)

        # RIGHT PANEL SLIDERS
        self.ball_h_max = tk.Scale(self.right_panel, from_=0, to=179, orient="horizontal",
                            label="H Max", command=self.on_slider_change)
        self.ball_s_max = tk.Scale(self.right_panel, from_=0, to=255, orient="horizontal",
                            label="S Max", command=self.on_slider_change)
        self.ball_v_max = tk.Scale(self.right_panel, from_=0, to=255, orient="horizontal",
                            label="V Max", command=self.on_slider_change)

        self.ball_h_max.place(x=20+100, y=20+20, width=100)
        self.ball_s_max.place(x=20+100, y=90+20, width=100)
        self.ball_v_max.place(x=20+100, y=160+20, width=100)

        # DEFAULTS
        self.ball_h_max.set(179)
        self.ball_s_max.set(255)
        self.ball_v_max.set(255)

        self.wall_h_max.set(179)
        self.wall_s_max.set(255)
        self.wall_v_max.set(255)

        # BUTTONS
        save_btn = tk.Button(self.left_panel, text="Save HSV", command=self.save_hsv_values)
        save_btn.place(x=20, y=240, width=200, height=40)

        exit_btn = tk.Button(self.right_panel, text="Exit", command=self.exit)
        exit_btn.place(x=20, y=240, width=200, height=40)


    def on_slider_change(self, value):
        print(f"Slider value {value}")

    def gui_update(self):
        self.update_idletasks()
        self.update()

        button_actions = {
            "save": (True, "save"),
            "exit": (False, self.selected_button)
        }

        result = button_actions.get(self.selected_button, (True, "none"))
        self.selected_button = "none" # Reset after handling
        return result

    def get_wall_hsv_values(self):
        self.wall_hsv = [self.wall_h_min.get(), self.wall_s_min.get(), self.wall_v_min.get(), self.wall_h_max.get(), self.wall_s_max.get(), self.wall_v_max.get()]
        return self.wall_hsv
    
    def get_ball_hsv_values(self):
        self.ball_hsv = [self.ball_h_min.get(), self.ball_s_min.get(), self.ball_v_min.get(), self.ball_h_max.get(), self.ball_s_max.get(), self.ball_v_max.get()]
        return self.ball_hsv
    
    def get_mode(self): return "None"
    def save_hsv_values(self): self.selected_button = "save"
    def exit(self): self.selected_button = "exit"; self.close()
    def close(self): self.destroy()

    