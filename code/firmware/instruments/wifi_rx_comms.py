import socket
import time

class WIFI_Client:
    def __init__(self, host, port):
        self.hostname = host
        self.port = port

    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.hostname, self.port))
                print(f"Connected to server at {self.hostname}:{self.port}")

                message = "Hello from Pi over WIFI!"
                s.sendall(message.encode('utf-8'))

                data = s.recv(1024)
                print(f"Received fom server : {data.decode('utf-8')}")

            except ConnectionRefusedError:
                print("Connection refused!")