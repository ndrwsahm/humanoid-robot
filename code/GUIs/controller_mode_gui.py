import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame as pg

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
    6: (True, "Back"),
    7: (True, "Start"),
    8: (True, "Xbox"),
}

class Controller_Mode_GUI:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("Controller Mode Example")
        self.root.geometry(str(width) + "x" + str(height))

        self.width = width
        self.height = height

        self.exit_application = False
        self.selected_button = "none"
        self.last_button = "none"
        self.key_pressed = None

        self.load_widgets()
        self.xbox_img = self.load_image(400, 300, "assets/xbox_controller.png")
        self.place_image(50, 50)

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

    def place_image(self, x, y):
        label = tk.Label(self.root, image=self.xbox_img)
        label.image = self.xbox_img
        label.place(x=x, y=y)

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
        button = tk.Button(self.root, text=text, bg=color, fg="white", font=("Arial", 14),
                         width=width, height=height, command=command)
    
        button.place(x=x, y=y)
        return button
    
    def update(self):
        if self.exit_application:
            return False, self.selected_button
        else:
            self.root.update_idletasks()
            self.root.update()
            
            if self.exit_application:
                return False, self.selected_button
        
            self.button = self.events()
            result = BUTTON_NAMES.get(self.button, (True, "none"))
            
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
        self.root.destroy()
        self.exit_application = True
        print("close")

    def exit_button_click(self): self.selected_button = "exit"; self.close()
