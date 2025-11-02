import sys
import select
import os

firmware_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, firmware_dir)

from settings import *

class SSH_RX_Comms:
   def __init__(self):
       pass

   def close(self):
       pass    

   def get_user_input(self):
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.readline().strip()
        return None

   """   
   def parse_user_input(self, line):
      line = line.strip()
      parts = line.split()

      if len(parts) == 2:
         try:
               return {
                  "joint": parts[0],
                  "angle": float(parts[1])
               }
         except ValueError:
               return {"error": f"Invalid angle format: {parts[1]}"}
      elif len(parts) == 1:
         return {"error": f"Only joint received: {parts[0]}"}
      elif len(parts) == 0:
         return {"error": "Empty line received"}
      else:
         return {"error": f"Malformed line: {line}"}
    """
if __name__ == "__main__":
   rx = SSH_RX_Comms()

   while True:
      rx.get_user_input()
   
