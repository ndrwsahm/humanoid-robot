import tkinter as tk
from tkinter import ttk
from GUIs.tool_tip_gui import ToolTip

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2

class Startup_GUI(tk.Frame):
    def __init__(self, width, height, hostname, username, location, com_port, baudrate, parent_root):
        super().__init__(parent_root)

        self.width = width
        self.height = height
        self.config(width=self.width, height=self.height)
        self.pack_propagate(False)

        # Stored values
        self.hostname = hostname
        self.username = username
        self.location = location
        self.com_port = com_port
        self.baudrate = baudrate

        # State
        self.exit_application = False
        self.selected_button = "none"
        self.robot_servo_connection = False
        self.robot_camera_connection = False

        # Layout columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.load_widgets()

    # ----------------------------------------------------------
    # BUILD LAYOUT
    # ----------------------------------------------------------
    def load_widgets(self):

        # LEFT COLUMN
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="n", padx=20, pady=20)

        self.create_pi_selector(left)
        self.create_ssh_section(left)

        # CENTER COLUMN
        center = tk.Frame(self)
        center.grid(row=0, column=1, sticky="n", padx=20, pady=20)

        self.create_firmware_buttons(center)
        self.create_command_entry(center)

        # RIGHT COLUMN
        right = tk.Frame(self)
        right.grid(row=0, column=2, sticky="n", padx=20, pady=20)

        left.grid_propagate(False)
        center.grid_propagate(False)
        right.grid_propagate(False)

        left.config(width=400, height=500)
        center.config(width=400, height=500)
        right.config(width=400, height=500)

        self.create_simulate_scale(right)
        #self.create_recal_scale(right)
        #self.create_nrf_buttons(right)
        self.create_mode_buttons(right)
        self.create_command_reference(left)

    # ----------------------------------------------------------
    # LEFT COLUMN
    # ----------------------------------------------------------
    def create_pi_selector(self, parent):
        tk.Label(parent, text="Select Pi").grid(row=0, column=0, pady=(0,5))
        self.pi_selector_scale = ttk.Scale(parent, from_=0, to=1, orient="horizontal")
        self.pi_selector_scale.grid(row=1, column=0, pady=5)
        tk.Label(parent, text="Pi 3        Pi Zero").grid(row=2, column=0)

    def create_ssh_section(self, parent):
        self.ip_label = tk.Label(parent, text=f"IP Addr: {self.hostname}")
        self.ip_label.grid(row=3, column=0, pady=(20,0))

        self.username_label = tk.Label(parent, text=f"Username: {self.username}")
        self.username_label.grid(row=4, column=0)

        self.ssh_button = tk.Button(
            parent, text="SSH Connect", bg="blue", fg="white", font=("Arial", 14),
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.ssh_button_click
        )
        self.ssh_button.grid(row=5, column=0, pady=10)

        # Small frame to isolate SSH indicators
        ssh_status_frame = tk.Frame(parent)
        ssh_status_frame.grid(
            row=5,
            column=0,
            columnspan=2,   # spans both columns
            sticky="w",     # push it toward the right edge (between columns)
            padx=(295, 0)    # adjust horizontal offset
        )
        
        self.ssh_pi_camera_indicator = tk.Button(
            ssh_status_frame, text="No SSH", bg="red", fg="white",
            font=("Arial", 10), width=12, height=1
        )
        self.ssh_pi_camera_indicator.grid(row=0, column=0, pady=5)

        self.ssh_pi_servo_indicator = tk.Button(
            ssh_status_frame, text="No SSH", bg="red", fg="white",
            font=("Arial", 10), width=12, height=1
        )
        self.ssh_pi_servo_indicator.grid(row=1, column=0, pady=5)

    # ----------------------------------------------------------
    # CENTER COLUMN
    # ----------------------------------------------------------
    def create_firmware_buttons(self, parent):
        self.file_path_label = tk.Label(parent, text=f"File Location: {self.location}")
        self.file_path_label.grid(row=0, column=0, pady=(0,10))

        buttons = [
            ("Install Firmware", self.firmware_button_click),
            ("Uninstall Firmware", self.uninstall_firmware_button_click),
            ("Test Accelerometer", self.test_accelerometer_button_click),
            ("Test Camera", self.test_camera_button_click),
            ("Run Raspi Config", self.run_raspi_config_button_click),
            ("Reboot Pi", self.run_reboot_button_click),
        ]

        for i, (text, cmd) in enumerate(buttons, start=1):
            tk.Button(
                parent, text=text, bg="blue", fg="white", font=("Arial", 12),
                width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                command=cmd
            ).grid(row=i, column=0, pady=5)

    def create_command_entry(self, parent):
        tk.Label(parent, text="Command Line Argument").grid(row=10, column=0, pady=(20,5))

        self.cmd_line_arg = tk.StringVar()
        #tk.Entry(parent, textvariable=self.cmd_line_arg, font=("Arial", 14)).grid(row=11, column=0)
        self.cmd_line_entry = tk.Entry(parent, textvariable=self.cmd_line_arg, font=("Arial", 14))
        self.cmd_line_entry.grid(row=11, column=0)

        tk.Button(
            parent, text="Send", bg="blue", fg="white", 
            width=10, command=self.send_button_click
        ).grid(row=12, column=0, pady=5)

    # ----------------------------------------------------------
    # RIGHT COLUMN
    # ----------------------------------------------------------
    def create_simulate_scale(self, parent):
        tk.Label(parent, text="Simulate").grid(row=0, column=0, pady=(0,5))

        frame = tk.Frame(parent)
        frame.grid(row=1, column=0)

        tk.Label(frame, text="True").grid(row=0, column=0, padx=5)
        self.simulate_scale = ttk.Scale(frame, from_=0, to=1, orient="horizontal")
        self.simulate_scale.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="False").grid(row=0, column=2, padx=5)

    def create_recal_scale(self, parent):
        tk.Label(parent, text="Recal Servos").grid(row=2, column=0, pady=(20,5))

        frame = tk.Frame(parent)
        frame.grid(row=3, column=0)

        tk.Label(frame, text="True").grid(row=0, column=0, padx=5)
        self.recal_scale = ttk.Scale(frame, from_=0, to=1, orient="horizontal")
        self.recal_scale.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="False").grid(row=0, column=2, padx=5)

    def create_nrf_buttons(self, parent):
        tk.Button(
            parent, text="NRF Connect", bg="red", fg="white",
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.nrf_button_click
        ).grid(row=4, column=0, pady=10)

        tk.Label(parent, text=f"Baudrate: {self.baudrate}").grid(row=5, column=0)
        tk.Label(parent, text=f"Com Port: {self.com_port}").grid(row=6, column=0)

    def create_mode_buttons(self, parent):
        tk.Button(
            parent, text="Manual Control", bg="green", fg="white", font=("Arial", 14),
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.manual_control_button_click
        ).grid(row=7, column=0, pady=(30,5))

        tk.Button(
            parent, text="Controller Mode", bg="green", fg="white", font=("Arial", 14),
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.controller_mode_button_click
        ).grid(row=8, column=0, pady=5)

        tk.Button(
            parent, text="Calibrate Servos", bg="green", fg="white", font=("Arial", 14),
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.calibrate_servos_button_click
        ).grid(row=9, column=0, pady=10)

        tk.Button(
            parent, text="Exit", bg="green", fg="white", font=("Arial", 14),
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            command=self.exit_button_click
        ).grid(row=10, column=0, pady=20)

    def create_command_reference(self, parent):
        tk.Label(parent, text="Pi Diagnostic Commands").grid(row=10, column=0, pady=(30,5))

        frame = tk.Frame(parent)
        frame.grid(row=11, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Listbox
        self.cmd_listbox = tk.Listbox(
            frame, height=10, width=40,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10)
        )
        self.cmd_listbox.pack(side="left", fill="both")

        scrollbar.config(command=self.cmd_listbox.yview)

        # Commands to populate
        commands = [
            "vcgencmd get_throttled",
            "vcgencmd measure_temp",
            "vcgencmd get_camera",
            "vcgencmd get_mem gpu",
            "vcgencmd get_mem arm",
            "dmesg | grep -i voltage",
            "dmesg | grep -i camera",
            "i2cdetect -y 1",
            "ls /dev/video*",
            "lsusb",
            "top",
            "htop",
            "free -h",
            "df -h",
            "sudo systemctl restart camera",
            "sudo systemctl restart networking",
            "sudo reboot",
            "sudo shutdown now"
        ]

        # Descriptions for each command (can be used for tooltips or a reference section)
        descriptions = {
            "vcgencmd get_throttled": "Shows undervoltage and throttling flags.",
            "vcgencmd measure_temp": "Reads CPU temperature.",
            "vcgencmd get_camera": "Checks if the camera module is detected and enabled.",
            "vcgencmd get_mem gpu": "Shows GPU memory allocation.",
            "vcgencmd get_mem arm": "Shows ARM CPU memory allocation.",
            "dmesg | grep -i voltage": "Searches system logs for voltage warnings.",
            "dmesg | grep -i camera": "Searches logs for camera errors.",
            "i2cdetect -y 1": "Scans I²C bus for connected devices.",
            "ls /dev/video*": "Lists available video devices.",
            "lsusb": "Lists USB devices.",
            "top": "Shows real-time CPU and memory usage.",
            "htop": "Improved system monitor (if installed).",
            "free -h": "Shows RAM usage in human-readable format.",
            "df -h": "Shows disk usage.",
            "sudo systemctl restart camera": "Restarts the camera service.",
            "sudo systemctl restart networking": "Restarts networking services.",
            "sudo reboot": "Reboots the Raspberry Pi.",
            "sudo shutdown now": "Shuts down the Raspberry Pi immediately."
        }

        for cmd in commands:
            self.cmd_listbox.insert(tk.END, cmd)

        # Attach tooltips to each listbox item
        for i, cmd in enumerate(commands):
            item_id = self.cmd_listbox  # listbox itself is the widget
            ToolTip(item_id, descriptions.get(cmd, "No description available"))

        # Optional: click-to-copy behavior
        def copy_command(event):
            selection = self.cmd_listbox.get(tk.ACTIVE)
            self.cmd_line_arg.set(selection)

        self.cmd_listbox.bind("<Double-Button-1>", copy_command)

        def on_motion(event):
            index = self.cmd_listbox.nearest(event.y)
            if 0 <= index < len(commands):
                cmd = commands[index]
                tooltip.text = descriptions.get(cmd, "")
            else:
                tooltip.text = ""

        tooltip = ToolTip(self.cmd_listbox, "")
        self.cmd_listbox.bind("<Motion>", on_motion)

    # ----------------------------------------------------------
    # UPDATE LOOP + STATE
    # ----------------------------------------------------------
    def gui_update(self):
        if self.exit_application:
            return False, self.selected_button

        self.update_idletasks()
        self.update()

        if self.exit_application:
            return False, self.selected_button

        self.update_simulate_scale()
        pi_selection = self.get_pi_selector_value()
        self.update_hostname(pi_selection)
        self.update_username(pi_selection)
        self.update_location(pi_selection)

        # Update SSH indicator
        if self.robot_servo_connection:
            self.ssh_pi_servo_indicator.config(
                text=f"Servo Pi",
                bg="green"
            )
        else:
            self.ssh_pi_servo_indicator.config(
                text="No SSH",
                bg="red"
            )

        if self.robot_camera_connection:
            self.ssh_pi_camera_indicator.config(
                text=f"Camera Pi",
                bg="green"
            )
        else:
            self.ssh_pi_camera_indicator.config(
                text="No SSH",
                bg="red"
            )

        button_actions = {
            "ssh": (True, "ssh"),
            #"nrf": (True, "nrf"),
            "send": (True, "send"),
            "uninstall_firmware": (True, "uninstall_firmware"),
            "firmware": (True, "firmware"),
            "run_firmware": (True, "run_firmware"),
            "test_accelerometer": (True, "test_accelerometer"),
            "test_camera": (True, "test_camera"),
            "manual_control": (True, "manual_control"),
            "controller_mode": (True, "controller_mode"),
            "calibrate_servos": (True, "calibrate_servos"),
            "raspi_config": (True, "raspi_config"),
            "reboot": (True, "reboot")
        }

        result = button_actions.get(self.selected_button, (True, "none"))
        self.selected_button = "none"
        return result

    # ----------------------------------------------------------
    # VALUE GETTERS
    # ----------------------------------------------------------
    def get_command(self):
        cmd = self.cmd_line_arg.get()
        self.cmd_line_entry.delete(0, tk.END)
        return cmd + "\n"

    def update_simulate_scale(self):
        if self.robot_servo_connection:
            self.simulate_scale.set(1)
            self.ssh_button.configure(bg="green")
        else:
            self.simulate_scale.set(0)
            self.ssh_button.configure(bg="red")
            #self.nrf_button.configure(bg="red")

    def update_hostname(self, new_hostname):
        self.hostname = new_hostname
        self.ip_label.config(text=f"IP Addr: {self.hostname}")

    def update_username(self, new_username):
        self.username = new_username
        self.username_label.config(text=f"Username: {self.username}")
  
    def update_location(self, new_location):
        self.location = new_location
        self.file_path_label.config(text=f"File Location: {self.location}")

    def get_pi_selector_value(self):
        val = self.pi_selector_scale.get()
        self.pi_selector_scale.set(1 if val >= 0.5 else 0)
        return "pi_robot" if val >= 0.5 else "pi_camera"

    def get_simulate_value(self):
        val = self.simulate_scale.get()
        self.simulate_scale.set(1 if val >= 0.5 else 0)
        return False if val >= 0.5 else True

    def get_recal_value(self):
        val = self.recal_scale.get()
        self.recal_scale.set(1 if val >= 0.5 else 0)
        return False if val >= 0.5 else True

    # ----------------------------------------------------------
    # BUTTON CALLBACKS
    # ----------------------------------------------------------
    def close(self):
        self.destroy()
        self.exit_application = True

    def ssh_button_click(self): self.selected_button = "ssh"
    def calibrate_servos_button_click(self): self.selected_button = "calibrate_servos"
    #def nrf_button_click(self): self.selected_button = "nrf"
    def manual_control_button_click(self): self.selected_button = "manual_control"
    def controller_mode_button_click(self): self.selected_button = "controller_mode"
    def send_button_click(self): self.selected_button = "send"
    def firmware_button_click(self): self.selected_button = "firmware"
    def run_firmware_button_click(self): self.selected_button = "run_firmware"
    def uninstall_firmware_button_click(self): self.selected_button = "uninstall_firmware"
    def run_raspi_config_button_click(self): self.selected_button = "raspi_config"
    def run_reboot_button_click(self): self.selected_button = "reboot"
    def test_accelerometer_button_click(self): self.selected_button = "test_accelerometer"
    def test_camera_button_click(self): self.selected_button = "test_camera"
    def exit_button_click(self): self.selected_button = "exit"; self.close()
