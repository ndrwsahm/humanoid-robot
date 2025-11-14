import sys
import serial
import os

firmware_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, firmware_dir)

from settings import *

class Serial_RX_Comms:
   def __init__(self):
      self.ser = None

      try:
         self.ser = serial.Serial(PI_COM_PORT, PI_BAUDRATE, timeout=1)
         print(f"Connected to {PI_COM_PORT} at {PI_BAUDRATE} baud.")
      except serial.SerialException as e:
         print("Serial connection failed: ", e)
      except KeyboardInterrupt:
         print("Serial listener stopped")

   def close(self):
      if self.ser and self.ser.is_open:
         self.ser.close()       

   def get_user_input(self):
      try:
         if self.ser.in_waiting and self.ser:
            line = self.ser.readline().decode('utf-8', errors='ignore')
            #result = self.parse_user_input(line)
            #print(line)
            #if "error" in result:
            #   print("Error:", result["error"])
            #else:
            #   print(f"Joint: {result['joint']}, Angle: {result['angle']}")

            #return result
            return line.replace(" ", "") # Remove spaces between command
      except Exception as e:
         pass

if __name__ == "__main__":
   rx = Serial_RX_Comms()

   while True:
      rx.get_user_input()
   