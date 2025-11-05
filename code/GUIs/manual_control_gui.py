import tkinter as tk
from tkinter import ttk
from globals import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Manual_Control_GUI:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("Slider Example")
        self.root.geometry(str(width) + "x" + str(height))
        
        #self.root.columnconfigure(1, weight=1)
        #self.root.columnconfigure(2, weight=1)
        #self.root.columnconfigure(4, weight=1)
        #self.root.columnconfigure(5, weight=1)

        self.width = width
        self.height = height

        self.exit_application = False

        self.load()
        self.new([90,90,90,90,90,90,90,90,90,90,90,90], [-9, 0, 12.25, -9, 0, 12.25])

        self.mode = "Angles"

    def load(self):
        self.leg_slider_angle_group = []
        self.leg_label_angle_group = []
        self.leg_text_angle_group = ["Left Hip Rotator: ", "Left Hip Aductor: ", "Left Hip Extendor: ", "Left Knee: ", "Left Ankle Aductor: ", "Left Ankle Extendor: ", "Right Hip Rotator: ", "Right Hip Aductor: ", "Right Hip Extendor: ", "Right Knee: ", "Right Ankle Aductor: ", "Right Ankle Extendor: "]
        # Anlge Track Sliders
        for al in ALL_LEGS:
            self.leg_slider_angle_group.append(ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_angle_value(al)))
            self.leg_label_angle_group.append(tk.Label(self.root, text=self.leg_text_angle_group[al], width=35))

        self.empty_label = tk.Label(self.root, text = "")

        self.leg_slider_pos_group = []
        self.leg_label_pos_group = []
        self.leg_text_pos_group = ["Left Foot X Position:  ", "Left Foot Y Position: ", "Left Foot Z Position: ", "Right Foot X Position: ", "Right Foot Y Position: ", "Right Foot Z Position: "]

        for al in ALL_POS:
            self.leg_slider_pos_group.append(ttk.Scale(self.root, from_=MIN_POS[al], to=MAX_POS[al], orient="horizontal", command=lambda x: self.get_slider_pos_value(al)))
            self.leg_label_pos_group.append(tk.Label(self.root, text=self.leg_text_pos_group[al], width=35))

        mode_button = tk.Button(self.root, text="Mode", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.mode_button_click)
        mode_button.place(x=150, y=450)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=450, y=450)

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

        self.empty_label = tk.Label(self.root, text="           ")
        self.empty_label.grid(row=3,column=3,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
   
    def hide_kinematic_sliders(self):
        for al in ALL_POS:
            self.leg_slider_pos_group[al].grid_remove()
            self.leg_label_pos_group[al].grid_remove()
      
    def show_angle_sliders(self):
        for j in range(6): # number of servos per leg
            self.leg_slider_angle_group[j].grid(row=j, column=1, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_slider_angle_group[j+6].grid(row=j, column=4, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

            self.leg_label_angle_group[j].grid(row=j, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
            self.leg_label_angle_group[j+6].grid(row=j, column=5, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

        self.empty_label = tk.Label(self.root, text="           ")
        self.empty_label.grid(row=3,column=3,padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)

    def hide_angle_sliders(self):
        for al in ALL_LEGS:
            self.leg_slider_angle_group[al].grid_remove()
            self.leg_label_angle_group[al].grid_remove()

    def update(self):
        self.root.update_idletasks()
        self.root.update()

        if self.mode == "Kinematics":
            self.hide_angle_sliders()
            self.show_kinematic_sliders()
        elif self.mode == "Angles":
            self.hide_kinematic_sliders()
            self.show_angle_sliders()
        
        if self.exit_application:
            return False, self.selected_button
        else:
            return True, "none"

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
    
    def get_mode(self):
        return self.mode

    def exit_button_click(self):
        self.selected_button = "exit"
        self.close()

    def mode_button_click(self):
        if self.mode == "Kinematics":
            self.mode = "Angles"

        elif self.mode == "Angles":
            self.mode = "Kinematics"

        self.selected_button = "mode"

    def close(self):
        #self.root.quit()
        self.root.destroy()
        self.exit_application = True
   
