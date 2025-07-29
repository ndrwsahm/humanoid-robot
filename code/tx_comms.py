import time
import paramiko

from globals import *

class TX_Comms:
    def __init__(self):
        self.host_name = HOSTNAME
        self.username = USERNAME
        self.password = PASSWORD

        self.file_location_on_pi = FIRMWARE_REMOTE_LOCATION

        self.connection = False

        self.load()
        self.new()

    def new(self):
        pass

    def load(self):
        """
        arg1 = ' --left_led_red ' + str(self.left_led_red_pin)
        arg2 = ' --left_led_green ' + str(self.left_led_green_pin)
        arg3 = ' --left_led_blue ' + str(self.left_led_blue_pin)
        """
        pass

    def update(self, command):
        self.send_command(command)
        self.response = self.receive_response()

    def connect_ssh(self):
        attempts = 0

        print("\nConnecting SSH...\n")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(" Connecting to " + self.host_name + " and username: " + self.username)
        try:
            self.ssh.connect(hostname=self.host_name, username=self.username, password=self.password)

            time.sleep(0.5)

            # Need to run script to wait for user input
            #full_file_path = 'sudo python ' + self.file_location_on_pi + '\n'
            #print("Running file at the following location: " + 'python ' + self.file_location_on_pi + "\n")

            #print("Args Sent..." + self.firmware_args)

            #self.channel.send(full_file_path)
            stdin, stdout, stderr = self.ssh.exec_command("ls")
            print(stdout.readlines())
            return True
 
        except:
            print("Unable to Connect!")
            return False

    def send_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print(stdout.readlines())

    def test_comms(self):
        full_file_path = 'sudo python ' + self.file_location_on_pi + 'test_comms.py\n'
        print(full_file_path)

    def install_firmware(self, from_local_path, to_remote_path):
        try:
            sftp = self.ssh.open_sftp()
            local_file_path = from_local_path + "local_file.txt"
            #local_file_path = "C:\\Users\\andre\\Github\\humanoid-robot\\code\\firmware\\local_file.txt"
            #"/home/humanoid39/Documents/firmware/"
            #remote_file_path = '/home/humanoid39/Documents/remote_file.txt'
            remote_file_path = to_remote_path + "remote_file.txt"
            sftp.put(local_file_path, remote_file_path)
            print(f"File {local_file_path} uploaded to {remote_file_path} successfully.")
            sftp.close()
        except Exception as e:
            print(e)

    def receive_response(self):
        pass

    def close(self):
        self.channel.send('quit\n')
        self.channel.close()
        self.ssh.close()
