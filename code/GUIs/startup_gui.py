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
        self.selected_button = "none"

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

        SSH_BUTTON_X = 200
        SSH_BUTTON_Y = 75
        self.ssh_button = tk.Button(self.root, text="Connect to PI", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.ssh_button_click)
        self.ssh_button.place(x=SSH_BUTTON_X, y=SSH_BUTTON_Y)
        self.ssh_button_label1 = tk.Label(self.root, text="IP Addr: "+str(HOSTNAME))
        self.ssh_button_label1.place(x=SSH_BUTTON_X-150, y=SSH_BUTTON_Y+10)
        self.ssh_button_label2 = tk.Label(self.root, text="Username: "+str(USERNAME))
        self.ssh_button_label2.place(x=SSH_BUTTON_X-150, y=SSH_BUTTON_Y+30)

        UNINSTALL_FIRMWARE_BUTTON_X = 10
        UNINSTALL_FIRMWARE_BUTTON_Y = 175
        self.uninstall_firmware_button = tk.Button(self.root, text="Uninstall Firmware", bg="red", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.uninstall_firmware_button_click)
        self.uninstall_firmware_button.place(x=UNINSTALL_FIRMWARE_BUTTON_X, y=UNINSTALL_FIRMWARE_BUTTON_Y)

        INSTALL_FIRM_BUTTON_X = 200
        INSTALL_FIRM_BUTTON_Y = 175
        self.firmware_button = tk.Button(self.root, text="Install Firmware", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.firmware_button_click)
        self.firmware_button.place(x=INSTALL_FIRM_BUTTON_X, y=INSTALL_FIRM_BUTTON_Y)
        self.firmware_button_label = tk.Label(self.root, text="File Location:   "+str(FIRMWARE_REMOTE_LOCATION))
        self.firmware_button_label.place(x=INSTALL_FIRM_BUTTON_X-150, y=SSH_BUTTON_Y+70)

        CMD_LINE_ENTRY_X = 10
        CMD_LINE_ENTRY_Y = 305
        self.cmd_line_label = tk.Label(self.root, text="Command Line Argument")
        self.cmd_line_label.place(x=CMD_LINE_ENTRY_X, y=CMD_LINE_ENTRY_Y-20)
        self.cmd_line_arg=tk.StringVar()
        self.cmd_line_entry = tk.Entry(self.root, textvariable=self.cmd_line_arg, font=("Arial", 14))
        self.cmd_line_entry.place(x=CMD_LINE_ENTRY_X, y=CMD_LINE_ENTRY_Y)

        SEND_BUTTON_X = 250
        SEND_BUTTON_Y = 300
        self.send_button = tk.Button(self.root, text="Send", bg="blue", fg="white", font=("Arial", 14), width=round(BUTTON_WIDTH/2), height=round(BUTTON_HEIGHT/2), command=self.send_button_click)
        self.send_button.place(x=SEND_BUTTON_X, y=SEND_BUTTON_Y)

        RUN_FIRM_BUTTON_X = 100
        RUN_FIRM_BUTTON_Y = 475
        self.run_firmware_button = tk.Button(self.root, text="Run Firmware", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.run_firmware_button_click)
        self.run_firmware_button.place(x=RUN_FIRM_BUTTON_X, y=RUN_FIRM_BUTTON_Y)

        RUN_CONFIG_BUTTON_X = 10
        RUN_CONFIG_BUTTON_Y = 375
        self.run_config_button = tk.Button(self.root, text="Run Raspi Config", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.run_raspi_config_button_click)
        self.run_config_button.place(x=RUN_CONFIG_BUTTON_X, y=RUN_CONFIG_BUTTON_Y)

        RUN_REBOOT_BUTTON_X = 200
        RUN_REBOOT_BUTTON_Y = 375
        self.run_reboot_button = tk.Button(self.root, text="Reboot Pi", bg="blue", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.run_reboot_button_click)
        self.run_reboot_button.place(x=RUN_REBOOT_BUTTON_X, y=RUN_REBOOT_BUTTON_Y)

        manual_control_button = tk.Button(self.root, text="Manual Control", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.manual_control_button_click)
        manual_control_button.place(x=525, y=175)

        exit_button = tk.Button(self.root, text="Exit", bg="green", fg="white", font=("Arial", 14), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=self.exit_button_click)
        exit_button.place(x=350, y=500)

    def update(self, connection):
        if self.exit_application:
            return False, self.selected_button
        else:
            self.root.update_idletasks()
            self.root.update()
            
            if self.exit_application:
                return False, self.selected_button
        
            self.update_ssh_button(connection)

            if self.selected_button == "ssh":
                self.selected_button = "none"   # Only send it once
                return True, "ssh"
            elif self.selected_button == "send":
                self.selected_button = "none"
                return True, "send"
            elif self.selected_button == "uninstall_firmware":
                self.selected_button = "none"
                return True, "uninstall_firmware"
            elif self.selected_button == "firmware":
                self.selected_button = "none"
                return True, "firmware"
            elif self.selected_button == "run_firmware":
                self.selected_button = "none"
                return True, "run_firmware"
            elif self.selected_button == "manual_control":
                self.selected_button = "none"
                return False, "manual_control"
            elif self.selected_button == "raspi_config":
                self.selected_button = "none"
                return True, "raspi_config"
            elif self.selected_button == "reboot":
                self.selected_button = "none"
                return True, "reboot"
            else:
                return True, "none"
        
    def manual_control_button_click(self):
        self.selected_button = "manual_control"
        self.close()

    def send_button_click(self):
        self.selected_button = "send"

    def get_command(self):
        cmd=self.cmd_line_arg.get()
        full_cmd = cmd + "\n"

        self.cmd_line_entry.delete(0, tk.END)

        return full_cmd

    def ssh_button_click(self):
        self.selected_button = "ssh"

    def update_ssh_button(self, connection):
        if not connection:
            self.simulate_scale.set(0)  
            self.ssh_button.configure(bg="red")
        else:
            self.simulate_scale.set(1) 
            self.ssh_button.configure(bg="green")

    def firmware_button_click(self):
        self.selected_button = "firmware"

    def run_firmware_button_click(self):
        self.selected_button = "run_firmware"

    def uninstall_firmware_button_click(self):
        self.selected_button = "uninstall_firmware"

    def run_raspi_config_button_click(self):
        self.selected_button = "raspi_config"

    def run_reboot_button_click(self):
        self.selected_button = "reboot"

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
        self.root.destroy()
        self.exit_application = True
        print("close")