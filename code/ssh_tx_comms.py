import time
import paramiko
import os

class SSH_TX_Comms:
    def __init__(self, hostname, username, password, location):
        self.host_name = hostname
        self.username = username
        self.password = password

        self.file_location_on_pi = location

        self.connection = False

        self.load()
        self.new()

    def new(self):
        pass

    def load(self):
        pass

    def update(self, command):
        self.send_user_input(command)
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

    def run_manual_control(self, file_path, rf_connection):
        # Need to run script to wait for user input
        if rf_connection:
            arg = 'nrf'
        else:
            arg = 'ssh'
        full_file_path = 'python3 ' + file_path + '/manual_control.py ' + arg + '\n'

        try:
            self.invoke_shell()
            print("Interactive shell started")
            self.send_user_input(full_file_path)
            print("Running file at the following location: " + full_file_path)

        except Exception as e:
            print (e)

    def run_firmware(self, file_path):
        # Need to run script to wait for user input
        full_file_path = 'python3 ' + file_path + '/firmware.py\n'

        try:
            self.invoke_shell()
            print("Interactive shell started")
            self.send_user_input(full_file_path)
            print("Running file at the following location: " + full_file_path)

        except Exception as e:
            print (e)

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

    def invoke_shell(self):
        try:
            self.channel = self.ssh.invoke_shell()
        except Exception as e:
            print (e)

    def send_user_input(self, command):
        try:
            self.channel.send(command)
        except Exception as e:
            print(e)

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
        output = None
        while self.channel.recv_ready():
            output = self.channel.recv(1024).decode('utf-8')

        if output:    
            return output

    def close(self):
        self.channel.send('quit\n')
        self.channel.close()
        self.ssh.close()
