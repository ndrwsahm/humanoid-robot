import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame as pg
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

BUTTON_NAMES = {
    0: (True, "walk_backward"),
    1: (True, "B"),
    2: (True, "X"),
    3: (True, "walk_forward"),
    4: (True, "LB"),
    5: (True, "RB") ,
    6: (True, "camera"),
    7: (True, "accel"),
    8: (True, "Xbox"),
}

class Controller_Mode_GUI(tk.Frame):
    def __init__(self, width, height, parent_root):
        super().__init__(parent_root) 

        self.width = width
        self.height = height

        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)

        self.exit_application = False
        self.selected_button = "none"
        self.last_button = "none"
        self.key_pressed = None

        self.canvas = tk.Canvas(self, width=500, height=400)
        self.canvas.pack(anchor=tk.NW)

        self.load_widgets()
        self.xbox_img = self.load_image(400, 300, "assets/xbox_controller.png")
        #self.place_image(50, 50)
        self.draw_image(0, 0)

        self.idx = 0

        # --- Initialize pygame for controller input ---
        pg.init()
        pg.joystick.init()

        self.controllers = {}
        self.rescan_controllers()

    def rescan_controllers(self):
        """Rescan and update controller list."""
        connected = pg.joystick.get_count()

        # Add new controllers
        for i in range(connected):
            if i not in self.controllers:
                joy = pg.joystick.Joystick(i)
                joy.init()
                self.controllers[i] = joy
                print(f"Connected: {joy.get_name()} (ID {i})")

        # Remove controllers that disappeared
        to_remove = []
        for i in self.controllers:
            if i >= connected:
                to_remove.append(i)

        for i in to_remove:
            print(f"Disconnected: ID {i}")
            del self.controllers[i]

    def draw_button_press(self, button):
        r = 10

        # Remove previous highlight
        if self.idx > 50000:
            self.canvas.delete("btn")
            self.idx = 0
            print("Cleared highlights")

        if button == 0:   # A
            x, y = 300, 115
            color = "green"
        elif button == 1: # B
            x, y = 325, 92
            color = "red"
        elif button == 2: # X
            x, y = 275, 90
            color = "blue"
        elif button == 3: # Y
            x, y = 300, 65
            color = "yellow"
        elif button == 4: # LB
            x, y = 100, 25
            color = "purple"
        elif button == 5: # RB
            x, y = 300, 25
            color = "orange"
        elif button == 6: # Back
            x, y = 175, 90
            color = "gray"
        elif button == 7: # Start
            x, y = 225, 90
            color = "gray"
        elif button == 8: # Xbox
            x, y = 200, 90
            color = "green"
        else:
            x, y = -100, -100  # Off-screen for unmapped buttons
            color = "black"
            self.idx += 1

        # Draw the new highlight
        self.canvas.create_oval(
            x-r, y-r, x+r, y+r,
            fill=color,
            outline="",
            tag="btn"
        )

    def draw_image(self, x, y):
        #self.canvas = tk.Canvas(self, width=self.xbox_img.width()+50, height=self.xbox_img.height()+50)
        #self.canvas.pack(anchor=tk.NW)
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.xbox_img)   
        
    def load_image(self, img_width, img_height, path):
        # Load and resize the image
        image = Image.open(path)
        image = image.resize((img_width, img_height), Image.ANTIALIAS)
        
        return ImageTk.PhotoImage(image)
    
    def load_widgets(self):
        self.create_all_buttons()

    def create_all_buttons(self):
        buttons = {
            "Exit":  (475, 500, "green", self.exit_button_click)
        }
        for text, (x, y, color, cmd) in buttons.items():
            self.create_button(text, x, y, color, cmd)

    def create_button(self, text, x, y, color, command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        button = tk.Button(self, text=text, bg=color, fg="white", font=("Arial", 14),
                         width=width, height=height, command=command)
    
        button.place(x=x, y=y)
        return button
    
    def gui_update(self):
        if self.exit_application:
            return False, self.selected_button
        else:
            self.update_idletasks()
            self.update()
            
            if self.exit_application:
                return False, self.selected_button

            # Gets button press
            self.button = self.events()
            self.draw_button_press(self.button)
            result = BUTTON_NAMES.get(self.button, (True, "none"))
            
            # Resets 
            self.selected_button = "none" # Reset after handling
            self.rescan_controllers()

            return result
        
    def events(self):
        button = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            # Get button press, Joysticks handled in update loop
            if event.type == pg.KEYDOWN:
                self.key_pressed = event.key
                print(f"Key pressed: {self.key_pressed}")

            if event.type == pg.JOYBUTTONDOWN:
                self.controller_number = event.joy  
                button = event.button
                print(f"Controller {self.controller_number} button pressed: {event.button}")
    
        return button
    
    def close(self):
        self.destroy()
        self.exit_application = True
        print("close")

    def exit_button_click(self): self.selected_button = "exit"; self.close()
