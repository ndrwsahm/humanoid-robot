import socket
import pickle
import cv2
from picamera2 import Picamera2
from libcamera import Transform

import subprocess

def get_throttled():
    try:
        out = subprocess.check_output(["vcgencmd", "get_throttled"]).decode().strip()
        return out
    except:
        return "throttled=ERROR"

class RPiCameraSender:
    def __init__(self, host="192.168.1.100", port=5000):
        try:
            self.picam2 = Picamera2()
            config = self.picam2.create_video_configuration(transform=Transform(vflip=True))
            self.picam2.configure(config)
            self.picam2.start()
        except Exception as e:
            print("CAMERA_INIT_FAILED:", e)
            print(subprocess.check_output(["vcgencmd", "get_throttled"]).decode())
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def stream_data(self):
        while True:
            try:
               frame = self.picam2.capture_array()
            except Exception as e:
                print(f"Error capturing frame: {e}")
                throttled = get_throttled()
                error_msg = {
                    "error": "CAMERA_CAPTURE_FAILED",
                    "throttled": throttled,
                    "exception": str(e)
                }
                payload = pickle.dumps(error_msg)
                self.sock.sendall(len(payload).to_bytes(4, "big"))
                self.sock.sendall(payload)
                continue

            # --- Compress frame as JPEG ---
            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                throttled = get_throttled()
                error_msg = {
                    "error": "ENCODE_FAILED",
                    "throttled": throttled
                }
                payload = pickle.dumps(error_msg)
                self.sock.sendall(len(payload).to_bytes(4, "big"))
                self.sock.sendall(payload)
                continue

            # Package metadata + compressed frame
            data = {"frame": buffer}

            # Serialize with pickle
            payload = pickle.dumps(data)

            # Send length prefix + payload
            self.sock.sendall(len(payload).to_bytes(4, "big"))
            self.sock.sendall(payload)

    def cleanup(self):
        self.picam2.stop()
        self.sock.close()

if __name__ == "__main__":
    sender = RPiCameraSender(host="192.168.1.151", port=5000)
    sender.stream_data()