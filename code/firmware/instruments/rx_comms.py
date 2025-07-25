import sys
import socket
import select

class RX_Comms:
   def __init__(self):
      """
      self.port = args.port
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_socket.bind(('', self.port))
      self.server_socket.listen(1)
      self.client_socket, self.computer_hostname = self.server_socket.accept()
      """
      pass

   def new(self):
      pass

   def load(self):
      pass

   def update(self):
      self.get_user_input()
   
   def get_user_input(self):
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.readline().strip()
        return None
   
   def parse_user_input(self, user_input):
      """
      user_input_2_chars = user_input[0:2]
      user_input_3_chars = user_input[0:3]
      """
      pass