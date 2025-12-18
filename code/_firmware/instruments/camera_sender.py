import socket
import pickle
import cv2
from picamera2 import Picamera2

class RPiCameraSender:
    def __init__(self, host="192.168.1.100", port=5000):
        self.picam2 = Picamera2()
        self.picam2.start()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def stream_data(self):
        while True:
            frame = self.picam2.capture_array()

            # --- Compress frame as JPEG ---
            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                continue

            # Package metadata + compressed frame
            data = {
                "frame": buffer,   # compressed numpy array
            }

            # Serialize with pickle
            payload = pickle.dumps(data)

            # Send length prefix + payload
            self.sock.sendall(len(payload).to_bytes(4, "big"))
            self.sock.sendall(payload)

    def cleanup(self):
        self.picam2.stop()
        self.sock.close()

if __name__ == "__main__":
    sender = RPiCameraSender(host="192.168.1.163", port=5000)
    sender.stream_data()