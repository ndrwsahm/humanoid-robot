import time
import paramiko
import os

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

            stdin, stdout, stderr = self.ssh.exec_command("ls")
            print(stdout.readlines())

            return True
 
        except:
            print("Unable to Connect!")
            return False

    def run_firmware(self, file_path):
        # Need to run script to wait for user input
        full_file_path = 'python3 ' + file_path + '/firmware.py\n'
        print("Running file at the following location: " + full_file_path)
        #print("Args Sent..." + self.firmware_args)
        self.send_command(full_file_path)

    def run_config(self, file_path):
        print("Running chmod..")
        full_file_path = 'chmod +x ' + file_path + '/pi_config.sh'
        self.send_command(full_file_path)
        print("Chmod finished")

        print("Running bash...")
        full_file_path = 'bash ' + file_path + '/pi_config.sh'
        self.send_command(full_file_path)
        print("Bash finished")

    def run_reboot(self, file_path):
        print("Running chmod..")
        full_file_path = 'chmod +x ' + file_path + '/rebot.sh'
        self.send_command(full_file_path)
        print("Chmod finished")

        print("Running bash...May take several minutes be patient...")
        full_file_path = 'bash ' + file_path + '/pi_config.sh'
        self.send_command(full_file_path)
        print("Bash finished")

    def send_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print(stdout.readlines())

    def install_firmware(self, from_local_path, to_remote_path):
        try:
            sftp = self.ssh.open_sftp()

            if os.path.isfile(from_local_path):
                sftp.put(from_local_path, to_remote_path)
                print(f"File {from_local_path} uploaded to {to_remote_path} successfully.")
            elif os.path.isdir(from_local_path):
                try:
                    self.create_folder_if_not_exist(to_remote_path)
                    #sftp.mkdir(to_remote_path)
                    print(f"Remote Directory Created: {to_remote_path}")
                except IOError as e:
                    if "File exists" not in str(e):
                        print(f"Error creating remote directory {to_remote_path}: {e}")
                        return
                
                for item in os.listdir(from_local_path):
                    local_item_path = os.path.join(from_local_path, item)
                    remote_item_path = os.path.join(to_remote_path, item).replace("\\", "/")
                    self.install_firmware(local_item_path, remote_item_path)

            sftp.close()
        except Exception as e:
            print(e)

    def uninstall_firmware(self, remote_path):
        try:
            sftp = self.ssh.open_sftp()
            
            self.send_command("rm -r " + remote_path + "/*")
            self.send_command("rmdir -r " + remote_path + "\n")

            for item in os.listdir(remote_path):
                remote_item_path = os.path.join(remote_path, item).replace("\\", "/")
                self.install_firmware(remote_item_path)
            
            print(f"Removed Directory at {remote_path}")

            sftp.close()
        except Exception as e:
            print(e)

    def create_folder_if_not_exist(self, remote_path):
        self.send_command("mkdir -p " + remote_path)

    def create_file_if_not_exist(self, remote_path):
        self.send_command("touch " + remote_path + "\n")

    def receive_response(self):
        pass

    def close(self):
        self.channel.send('quit\n')
        self.channel.close()
        self.ssh.close()
