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

if __name__ == "__main__":
   rx = SSH_RX_Comms()

   while True:
      rx.get_user_input()
   
