from equipment.ssh_tx_comms import *

class SSHManager:
    def __init__(self):
        self.targets = {}      # name → SSH_TX_Comms instance
        self.tx_robot = None
        self.tx_camera = None
        self.tx_general = None

    def add_target(self, name, hostname, username, password, path):
        self.targets[name] = SSH_TX_Comms(hostname, username, password, path)

    def connect_all(self):
        for name, tx in self.targets.items():
            tx.connect_ssh()

    def select_general(self, name):
        self.tx_general = self.targets[name]
