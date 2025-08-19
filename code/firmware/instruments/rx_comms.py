import sys
import socket
import select

class RX_Comms:
   def __init__(self):
      pass

   def new(self):
      pass

   def load(self):
      pass

   def update(self):
      pass

   def get_user_input(self):
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.readline().strip()
        return None
   