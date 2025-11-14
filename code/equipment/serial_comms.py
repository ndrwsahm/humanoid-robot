import serial
import time
import os
import sys

firmware_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, firmware_dir)

from globals import *

DEBUG_PRINT_STATEMENT = False

class Serial_Comms:
    def __init__(self, port='COM6', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Allow time for connection to stabilize
            print(f"Connected to {self.port} at {self.baudrate} baud.")
            return True
        except serial.SerialException as e:
            print(f"Serial connection failed: {e}")
            return False

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            self.ser.reset_input_buffer()  # Clear old data
            full_cmd = command.strip() + '\n'
            self.ser.write(full_cmd.encode('utf-8'))
            if DEBUG_PRINT_STATEMENT: print(f"Sent from Transmitter Arduino: {command}")
            #time.sleep(0.1)
            return self.receive_response()
        else:
            print("Serial port is not open.")
            return None

    def receive_response(self):
        if self.ser and self.ser.is_open:
            try:
                #response = self.ser.readline()
                response = self.ser.readline().decode('utf-8').strip()
                joint, angle = response.split()
                if response:
                    
                    parts = response.split()
                    if len(parts) == 2:
                        joint, angle = parts
                        try:
                            angle = float(angle)
                            #print("Joint:", joint, "Angle:", angle)
                        except ValueError:
                            print("Invalid angle format:", angle)
                    else:
                        print("Malformed line:", response)
                
                    if DEBUG_PRINT_STATEMENT: print(f"Response from Humanoid Receiver: {response}")
                return joint, angle
            except Exception as e:
                print(e)
                print("Ensure to plug in RX arduino and try again!!")
        return None

    def close(self):
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                #print("Serial connection closed.")
        except Exception as e:
            print(e)

# Example usage
if __name__ == "__main__":
    comms = Serial_Comms(port=COM_PORT, baudrate=BAUDRATE)
    if comms.connect():
        comms.send_command("CMD 39 lhr 80.5")
        time.sleep(1)
        comms.send_command("CMD 39 lha 90")
        time.sleep(1)
        comms.send_command("CMD 39 rha 87.3")
        time.sleep(1)
        comms.close()
