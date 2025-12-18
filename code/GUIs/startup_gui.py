import tkinter as tk
from tkinter import ttk

COLUMN_WIDTH_PADDING = 20
ROW_HEIGHT_PADDING = 10

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Startup_GUI:
    def __init__(self, width, height, hostname, username, location, com_port, baudrate):
        self.root = tk.Tk()
        self.root.title("Starup Example")
        self.root.geometry(str(width) + "x" + str(height))

        self.width = width
        self.height = height

        self.hostname = hostname
        self.username = username
        self.location = location

        self.com_port = com_port
        self.baudrate = baudrate

        self.exit_application = False
        self.selected_button = "none"

        self.load_widgets()
        self.simulate_scale.set(0)

    def load_widgets(self):
        self.create_simulate_scale(500, 200)
        self.create_recal_scale(500, 375)
        self.create_ssh_section(200, 75)
        self.create_firmware_buttons()
        self.create_command_entry(10, 305)
        self.create_nrf_buttons(475, 75)
        self.create_misc_buttons()

    def create_simulate_scale(self, x, y):
        self.simulate_scale = ttk.Scale(self.root, from_=0, to=1, orient="horizontal", command=lambda x: self.get_simulate_value)
        self.simulate_scale.place(x=x, y=y)
        tk.Label(self.root, text="Simulate").place(x=x-15, y=y-25)
        tk.Label(self.root, text="True                        False").place(x=x-15, y=y+25)

    def create_recal_scale(self, x, y):
        self.recal_scale = ttk.Scale(self.root, from_=0, to=1, orient="horizontal", command=lambda x: self.get_recal_value)
        self.recal_scale.place(x=x, y=y)
        tk.Label(self.root, text="Recal Servos").place(x=x-15, y=y-25)
        tk.Label(self.root, text="True                        False").place(x=x-15, y=y+25)
        tk.Label(self.root, text="If True, it will remove offsets").place(x=x+125, y=y)
        self.recal_scale.set(1)

    def create_ssh_section(self, x, y):
        self.ssh_button = self.create_button("SSH Connect", x, y, "blue", self.ssh_button_click)
        tk.Label(self.root, text=f"IP Addr: {self.hostname}").place(x=x-150, y=y+10)
        tk.Label(self.root, text=f"Username: {self.username}").place(x=x-150, y=y+30)

    def create_firmware_buttons(self):
        buttons = {
            "Uninstall Firmware":   (10, 175, "red", self.uninstall_firmware_button_click),
            "Install Firmware":     (200, 175, "blue", self.firmware_button_click),
            "Test Accelerometer":   (10, 475, "blue", self.test_accelerometer_button_click),
            "Test Camera":          (200, 475, "blue", self.test_camera_button_click),
            "Run Raspi Config":     (10, 375, "blue", self.run_raspi_config_button_click),
            "Reboot Pi":            (200, 375, "blue", self.run_reboot_button_click),
            "Manual Control":       (475, 275, "green", self.manual_control_button_click),
            "Exit":                 (475, 500, "green", self.exit_button_click)
        }
        for text, (x, y, color, cmd) in buttons.items():
            self.create_button(text, x, y, color, cmd)

        tk.Label(self.root, text=f"File Location: {self.location}").place(x=50, y=145)

    def create_command_entry(self, x, y):
        tk.Label(self.root, text="Command Line Argument").place(x=x, y=y-20)
        self.cmd_line_arg = tk.StringVar()
        self.cmd_line_entry = tk.Entry(self.root, textvariable=self.cmd_line_arg, font=("Arial", 14))
        self.cmd_line_entry.place(x=x, y=y)
        self.create_button("Send", 250, 300, "blue", self.send_button_click, width=round(BUTTON_WIDTH/2), height=round(BUTTON_HEIGHT/2))

    def create_nrf_buttons(self, x, y):
        self.nrf_button = self.create_button("NRF Connect", x, y, "red", self.nrf_button_click)
        tk.Label(self.root, text=f"NRF Wireless Connection").place(x=x+180, y=y+10)
        tk.Label(self.root, text=f"Baudrate: {self.baudrate}  Com Port: {self.com_port}").place(x=x+180, y=y+30)
        
    def create_misc_buttons(self):
        pass  # Reserved for future expansion
    
    def create_button(self, text, x, y, color, command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        button = tk.Button(self.root, text=text, bg=color, fg="white", font=("Arial", 14),
                         width=width, height=height, command=command)
    
        button.place(x=x, y=y)
        return button

    def update(self, ssh_connection, rf_connection):
        if self.exit_application:
            return False, self.selected_button
        else:
            self.root.update_idletasks()
            self.root.update()
            
            if self.exit_application:
                return False, self.selected_button
        
            self.update_simulate_scale(ssh_connection, rf_connection)

            button_actions = {
                "ssh": (True, "ssh"),
                "nrf": (True, "nrf"),
                "send": (True, "send"),
                "uninstall_firmware": (True, "uninstall_firmware"),
                "firmware": (True, "firmware"),
                "run_firmware": (True, "run_firmware"),
                "test_accelerometer": (True, "test_accelerometer"),
                "test_camera": (True, "test_camera"),
                "manual_control": (False, "manual_control"),
                "raspi_config": (True, "raspi_config"),
                "reboot": (True, "reboot")

            }

            result = button_actions.get(self.selected_button, (True, "none"))
            self.selected_button = "none" # Reset after handling
            return result
        
    def get_command(self):
        cmd=self.cmd_line_arg.get()
        full_cmd = cmd + "\n"

        self.cmd_line_entry.delete(0, tk.END)

        return full_cmd

    def update_simulate_scale(self, ssh_connection, rf_connection):
        if ssh_connection:
            self.simulate_scale.set(1)  
            self.ssh_button.configure(bg="green")
        elif rf_connection:
            self.simulate_scale.set(1)
            self.nrf_button.configure(bg="green")
        else:
            self.simulate_scale.set(0) 
            self.ssh_button.configure(bg="red")
            self.nrf_button.configure(bg="red")

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
        
    def get_recal_value(self):
        recal_val = self.recal_scale.get()

        if recal_val >= 0.5:
            self.recal_scale.set(1)
        else:
            self.recal_scale.set(0)

        if recal_val == 1:
            return False
        else:
            return True

    def close(self):
        self.root.destroy()
        self.exit_application = True
        print("close")

        
    def ssh_button_click(self): self.selected_button = "ssh"
    def nrf_button_click(self): self.selected_button = "nrf"
    def manual_control_button_click(self): self.selected_button = "manual_control"; self.close()
    def send_button_click(self): self.selected_button = "send"
    def firmware_button_click(self): self.selected_button = "firmware"
    def run_firmware_button_click(self): self.selected_button = "run_firmware"
    def uninstall_firmware_button_click(self): self.selected_button = "uninstall_firmware"
    def run_raspi_config_button_click(self): self.selected_button = "raspi_config"
    def run_reboot_button_click(self): self.selected_button = "reboot"
    def test_accelerometer_button_click(self): self.selected_button = "test_accelerometer"
    def test_camera_button_click(self): self.selected_button = "test_camera"
    def exit_button_click(self): self.selected_button = "exit"; self.close()
