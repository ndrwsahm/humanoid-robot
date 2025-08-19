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

        self.width = width
        self.height = height

        self.exit_application = False

        self.load()
        self.new()

    def load(self):
        # Left Hip Track Sliders
        self.left_hip_rotator_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LHR_IDX))
        self.left_hip_rotator_sliders.grid(row=0, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_hip_rotator_label = tk.Label(self.root, text="Left Hip Rotator: 0.00")
        self.left_hip_rotator_label.grid(row=0, column=1)

        self.left_hip_aductor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LHA_IDX))
        self.left_hip_aductor_sliders.grid(row=1, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_hip_aductor_label = tk.Label(self.root, text="Left Hip Aductor: 0.00")
        self.left_hip_aductor_label.grid(row=1, column=1)

        self.left_hip_extendor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LHE_IDX))
        self.left_hip_extendor_sliders.grid(row=2, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_hip_extendor_label = tk.Label(self.root, text="Left Hip Extendor: 0.00")
        self.left_hip_extendor_label.grid(row=2, column=1)

        # Right Hip Track Sliders
        self.right_hip_rotator_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RHR_IDX))
        self.right_hip_rotator_sliders.grid(row=0, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_hip_rotator_label = tk.Label(self.root, text="Right Hip Rotator: 0.00")
        self.right_hip_rotator_label.grid(row=0, column=3)

        self.right_hip_aductor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RHA_IDX))
        self.right_hip_aductor_sliders.grid(row=1, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_hip_aductor_label = tk.Label(self.root, text="Right Hip Aductor: 0.00")
        self.right_hip_aductor_label.grid(row=1, column=3)

        self.right_hip_extendor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RHE_IDX))
        self.right_hip_extendor_sliders.grid(row=2, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_hip_extendor_label = tk.Label(self.root, text="Right Hip Extendor: 0.00")
        self.right_hip_extendor_label.grid(row=2, column=3)

        # Left Knee Track Sliders
        self.left_knee_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LK_IDX))
        self.left_knee_sliders.grid(row=3, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_knee_label = tk.Label(self.root, text="Left Knee: 0.00")
        self.left_knee_label.grid(row=3, column=1)

        self.left_ankle_aductor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LAA_IDX))
        self.left_ankle_aductor_sliders.grid(row=4, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_ankle_aductor_label = tk.Label(self.root, text="Left Ankle Aductor: 0.00")
        self.left_ankle_aductor_label.grid(row=4, column=1)

        self.left_ankle_extendor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(LAE_IDX))
        self.left_ankle_extendor_sliders.grid(row=5, column=0, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.left_ankle_extendor_label = tk.Label(self.root, text="Left Ankle Extendor: 0.00")
        self.left_ankle_extendor_label.grid(row=5, column=1)

        # Right Back Track Sliders
        self.right_knee_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RK_IDX))
        self.right_knee_sliders.grid(row=3, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_knee_label = tk.Label(self.root, text="Right Knee: 0.00")
        self.right_knee_label.grid(row=3, column=3)

        self.right_ankle_aductor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RAA_IDX))
        self.right_ankle_aductor_sliders.grid(row=4, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_ankle_aductor_label = tk.Label(self.root, text="Right Ankle Aductor: 0.00")
        self.right_ankle_aductor_label.grid(row=4, column=3)

        self.right_ankle_extendor_sliders = ttk.Scale(self.root, from_=0, to=180, orient="horizontal", command=lambda x: self.get_slider_value(RAE_IDX))
        self.right_ankle_extendor_sliders.grid(row=5, column=2, padx=COLUMN_WIDTH_PADDING, pady=ROW_HEIGHT_PADDING)
        self.right_ankle_extendor_label = tk.Label(self.root, text="Right Ankle Extendor: 0.00")
        self.right_ankle_extendor_label.grid(row=5, column=3)

        self.left_pos_label = tk.Label(self.root, text = "")
        self.left_pos_label.grid(row=6, column=1)

        # Left Leg Knee POS
        self.left_knee_pos_label = tk.Label(self.root, text = "Left Leg Knee")
        self.left_knee_pos_label.grid(row=7, column=1)

        self.left_knee_x_pos_label = tk.Label(self.root, text = "X Pos: 0.00")
        self.left_knee_x_pos_label.grid(row=8, column=1)

        self.left_knee_y_pos_label = tk.Label(self.root, text = "Y Pos: 0.00")
        self.left_knee_y_pos_label.grid(row=8, column=2)

        self.left_knee_z_pos_label = tk.Label(self.root, text = "Z Pos: 0.00")
        self.left_knee_z_pos_label.grid(row=8, column=3)

        # Right Leg Knee POS
        self.right_knee_pos_label = tk.Label(self.root, text = "Right Leg Knee")
        self.right_knee_pos_label.grid(row=9, column=1)

        self.right_knee_x_pos_label = tk.Label(self.root, text = "X Pos: 0.00")
        self.right_knee_x_pos_label.grid(row=10, column=1)

        self.right_knee_y_pos_label = tk.Label(self.root, text = "Y Pos: 0.00")
        self.right_knee_y_pos_label.grid(row=10, column=2)

        self.right_knee_z_pos_label = tk.Label(self.root, text = "Z Pos: 0.00")
        self.right_knee_z_pos_label.grid(row=10, column=3)

        # Left Leg Foot POS
        self.left_foot_pos_label = tk.Label(self.root, text = "Left Leg Foot")
        self.left_foot_pos_label.grid(row=11, column=1)

        self.left_foot_x_pos_label = tk.Label(self.root, text = "X Pos: 0.00")
        self.left_foot_x_pos_label.grid(row=12, column=1)

        self.left_foot_y_pos_label = tk.Label(self.root, text = "Y Pos: 0.00")
        self.left_foot_y_pos_label.grid(row=12, column=2)

        self.left_foot_z_pos_label = tk.Label(self.root, text = "Z Pos: 0.00")
        self.left_foot_z_pos_label.grid(row=12, column=3)

        # Right Leg Foot POS
        self.right_foot_pos_label = tk.Label(self.root, text = "Right Leg Foot")
        self.right_foot_pos_label.grid(row=13, column=1)

        self.right_foot_x_pos_label = tk.Label(self.root, text = "X Pos: 0.00")
        self.right_foot_x_pos_label.grid(row=14, column=1)

        self.right_foot_y_pos_label = tk.Label(self.root, text = "Y Pos: 0.00")
        self.right_foot_y_pos_label.grid(row=14, column=2)

        self.right_foot_z_pos_label = tk.Label(self.root, text = "Z Pos: 0.00")
        self.right_foot_z_pos_label.grid(row=14, column=3)

        exit_button = tk.Button(self.root, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=350, y=500)

    def new(self):
        self.left_hip_rotator_sliders.set(90)
        self.left_hip_aductor_sliders.set(90)
        self.left_hip_extendor_sliders.set(90)

        self.right_hip_rotator_sliders.set(90)
        self.right_hip_aductor_sliders.set(90)
        self.right_hip_extendor_sliders.set(90)

        self.left_knee_sliders.set(90)
        self.left_ankle_aductor_sliders.set(90)
        self.left_ankle_extendor_sliders.set(90)

        self.right_knee_sliders.set(90)
        self.right_ankle_aductor_sliders.set(90)
        self.right_ankle_extendor_sliders.set(90)

    def update(self):
        self.root.update_idletasks()
        self.root.update()
        
        if self.exit_application:
            return False, self.selected_button
        else:
            return True, "none"

    def get_slider_value(self, leg):
        slider_val = 0
        if leg == LHR_IDX:
            #print(f"Left Hip Rotator Servo Value: {self.left_hip_sliders.get()}")
            slider_val = round(self.left_hip_rotator_sliders.get(), 0)
            self.left_hip_rotator_label.config(text="Left Hip Rotator: " + str(round(slider_val, 2)))
        elif leg == LHA_IDX:
            #print(f"Left Hip Aductor Servo Value: {self.left_hip_aductor_sliders.get()}")
            slider_val = round(self.left_hip_aductor_sliders.get(), 0)
            self.left_hip_aductor_label.config(text="Left Hip Aductor: " + str(round(slider_val, 2)))
        elif leg == LHE_IDX:
            #print(f"Left Hip Extendor Servo Value: {self.left_hip_extendor_sliders.get()}")
            slider_val = round(self.left_hip_extendor_sliders.get(), 0)
            self.left_hip_extendor_label.config(text="Left Hip Extendor: " + str(round(slider_val, 2)))

        elif leg == RHR_IDX:
            #print(f"Right Hip Rotator Servo Value: {self.right_hip_sliders.get()}")
            slider_val = round(self.right_hip_rotator_sliders.get(), 0)
            self.right_hip_rotator_label.config(text="Right Hip Rotator: " + str(round(slider_val, 2)))
        elif leg == RHA_IDX:
            #print(f"Right Hip Aductor Servo Value: {self.right_hip_aductor_sliders.get()}")
            slider_val = round(self.right_hip_aductor_sliders.get(), 0)
            self.right_hip_aductor_label.config(text="Right Hip Aductor: " + str(round(slider_val, 2)))
        elif leg == RHE_IDX:
            #print(f"Right Hip Extendor Servo Value: {self.right_hip_extendor_sliders.get()}")
            slider_val = round(self.right_hip_extendor_sliders.get(), 0)
            self.right_hip_extendor_label.config(text="Right Hip Extendor: " + str(round(slider_val, 2)))

        elif leg == LK_IDX:
            #print(f"Left Knee Servo Value: {self.left_knee_sliders.get()}")
            slider_val = round(self.left_knee_sliders.get(), 0)
            self.left_knee_label.config(text="Left Knee: " + str(round(slider_val, 2)))
        elif leg == LAA_IDX:
            #print(f"Left Knee Aductor Servo Value: {self.left_ankle_aductor_sliders.get()}")
            slider_val = round(self.left_ankle_aductor_sliders.get(), 0)
            self.left_ankle_aductor_label.config(text="Left Knee Aductor: " + str(round(slider_val, 2)))
        elif leg == LAE_IDX:
            #print(f"Left Knee Extendor Servo Value: {self.left_ankle_extendor_sliders.get()}")
            slider_val = round(self.left_ankle_extendor_sliders.get(), 0)
            self.left_ankle_extendor_label.config(text="Left Knee Extendor: " + str(round(slider_val, 2)))

        elif leg == RK_IDX:
            #print(f"Right Knee Servo Value: {self.right_knee_sliders.get()}")
            slider_val = round(self.right_knee_sliders.get(), 0)
            self.right_knee_label.config(text="Right Knee: " + str(round(slider_val, 2)))
        elif leg == RAA_IDX:
            #print(f"Right Ankle Aductor Servo Value: {self.right_ankle_aductor_sliders.get()}")
            slider_val = round(self.right_ankle_aductor_sliders.get(), 0)
            self.right_ankle_aductor_label.config(text="Right Ankle Aductor: " + str(round(slider_val, 2)))
        elif leg == RAE_IDX:
            #print(f"Right Ankle Extendor Servo Value: {self.right_ankle_extendor_sliders.get()}")
            slider_val = round(self.right_ankle_extendor_sliders.get(), 0)
            self.right_ankle_extendor_label.config(text="Right Ankle Extendor: " + str(round(slider_val, 2)))

        return round(slider_val)
    
    def get_all_slider_angles(self):
        all_angles = []
        for al in ALL_LEGS:
            all_angles.append(self.get_slider_value(al))
    
        return all_angles
    
    def update_pos_labels(self, left_pos, right_pos):
        self.left_knee_x_pos_label.config(text="X Pos: " + str(round(left_pos[0][0], 2)))
        self.left_knee_y_pos_label.config(text="Y Pos: " + str(round(left_pos[0][1], 2)))
        self.left_knee_z_pos_label.config(text="Z Pos: " + str(round(left_pos[0][2], 2)))

        self.right_knee_x_pos_label.config(text="X Pos: " + str(round(right_pos[0][0], 2)))
        self.right_knee_y_pos_label.config(text="Y Pos: " + str(round(right_pos[0][1], 2)))
        self.right_knee_z_pos_label.config(text="Z Pos: " + str(round(right_pos[0][2], 2)))

        self.left_foot_x_pos_label.config(text="X Pos: " + str(round(left_pos[1][0], 2)))
        self.left_foot_y_pos_label.config(text="Y Pos: " + str(round(left_pos[1][1], 2)))
        self.left_foot_z_pos_label.config(text="Z Pos: " + str(round(left_pos[1][2], 2)))

        self.right_foot_x_pos_label.config(text="X Pos: " + str(round(right_pos[1][0], 2)))
        self.right_foot_y_pos_label.config(text="Y Pos: " + str(round(right_pos[1][1], 2)))
        self.right_foot_z_pos_label.config(text="Z Pos: " + str(round(right_pos[1][2], 2)))

    def exit_button_click(self):
        self.selected_button = "exit"
        self.close()

    def close(self):
        #self.root.quit()
        self.root.destroy()
        self.exit_application = True
   
