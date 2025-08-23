import socket

class WIFI_Server:
    def __init__(self, hostname, username, password, port):
        self.host_name = hostname
        self.username = username
        self.password = password

        self.port = port

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.host_name, self.port)
            s.listen()
            print(f"Server listening on {self.host_name}:{self.port}")

            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    print(f"Received from Pi: {message}")

                    response = f"Server received: {message}"
                    conn.sendall(response.encode('utf-8'))

