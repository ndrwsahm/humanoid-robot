import time
import paramiko

from globals import *

class TX_Comms:
    def __init__(self):
        self.host_name = HOSTNAME
        self.username = USERNAME
        self.password = PASSWORD

        self.file_location_on_pi = FILE_LOCATION

        self.load()

        self.connection = self.connect_ssh()   # start ssh
  
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
            self.channel = self.ssh.invoke_shell()

            time.sleep(0.5)

            full_file_path = 'sudo python ' + self.file_location_on_pi + '\n'
            print("Running file at the following location: " + 'python ' + self.file_location_on_pi + "\n")

            #print("Args Sent..." + self.firmware_args)

            self.channel.send(full_file_path)
        
        except:
            print("Unable to Connect!")
            return False

        while not self.channel.recv_ready() and attempts < 10:
            print("Sending file path to run, trying for the ", str(attempts), " time...")
            self.channel.send(full_file_path)
            attempts += 1
            time.sleep(0.5)

        time.sleep(20.0)    #wait for full setup completion TODO MORE ROBUST WAIT
 
        if self.channel.recv_ready():
            output = self.channel.recv(3*1024*1024).decode('utf-8')
            print(output)
            return True
        else:
            print("SSH Not Receive Ready or Connected")
            return False

    def send_command(self, commnad):
        pass

    def receive_response(self):
        pass

    def close(self):
        self.channel.send('quit\n')
        self.channel.close()
        self.ssh.close()
