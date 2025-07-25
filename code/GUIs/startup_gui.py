import tkinter as tk
from tkinter import ttk

from globals import *
from tx_comms import *

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Startup_GUI:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("Starup Example")
        self.root.geometry(str(width) + "x" + str(height))

        self.width = width
        self.height = height

        self.exit_application = False

        self.load()
        self.new()

    def new(self):
        self.simulate_scale.set(0)

    def load(self):
        SIMULATE_SCALE_X = 550
        SIMULATE_SCALE_Y = 100
        self.simulate_scale = ttk.Scale(self.root, from_=0, to=1, orient="horizontal", command=lambda x: self.get_simulate_value)
        self.simulate_scale.place(x=SIMULATE_SCALE_X, y=SIMULATE_SCALE_Y)
        self.simulate_scale_label1 = tk.Label(self.root, text="Simulate")
        self.simulate_scale_label1.place(x=SIMULATE_SCALE_X-15, y=SIMULATE_SCALE_Y-25)
        self.simulate_scale_label2 = tk.Label(self.root, text="True                        False")
        self.simulate_scale_label2.place(x=SIMULATE_SCALE_X-15, y=SIMULATE_SCALE_Y+25)

        SSH_BUTTON_X = 150
        SSH_BUTTON_Y = 75
        ssh_button = tk.Button(self.root, text="Connect to PI", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.ssh_button_click)
        ssh_button.place(x=SSH_BUTTON_X, y=SSH_BUTTON_Y)
        self.ssh_button_label1 = tk.Label(self.root, text="IP Addr: "+str(HOSTNAME))
        self.ssh_button_label1.place(x=SSH_BUTTON_X-125, y=SSH_BUTTON_Y+10)
        self.ssh_button_label2 = tk.Label(self.root, text="Username: "+str(USERNAME))
        self.ssh_button_label2.place(x=SSH_BUTTON_X-125, y=SSH_BUTTON_Y+30)

        manual_control_button = tk.Button(self.root, text="Manual Control", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.manual_control_button_click)
        manual_control_button.place(x=500, y=200)

        exit_button = tk.Button(self.root, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=350, y=500)

    def update(self):
        self.root.update_idletasks()
        self.root.update()

        if self.exit_application:
            return False, self.selected_button
        else:
            return True, "none"
        
    def manual_control_button_click(self):
        self.selected_button = "manual_control"
        self.close()

    def ssh_button_click(self):
        ssh_comms = TX_Comms()
        if not ssh_comms.connection:
            self.simulate_scale.set(0)   

    def exit_button_click(self):
        self.selected_button = "exit"
        self.close()
        
    def get_simulate_value(self):
        simulate_val = self.simulate_scale.get()
        if simulate_val >= 0.5:
            self.simulate_scale.set(1)
        else:
            self.simulate_scale.set(0)

        if simulate_val == 1:
            return False
        else:
            return True

    def close(self):
        #self.root.quit()
        self.root.destroy()
        self.exit_application = True
