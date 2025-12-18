import socket
import pickle
import cv2
import numpy as np
import time

class CameraReceiver:
    def __init__(self, host="0.0.0.0", port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        print("Waiting for connection...")
        self.conn, _ = self.sock.accept()
        print("Connected!")

        # FPS tracking
        self.prev_time = time.time()
        self.frame_count = 0
        self.fps = 0

    def receive_data(self):
        while True:
            # Read length prefix
            length_bytes = self.conn.recv(4)
            if not length_bytes:
                break
            length = int.from_bytes(length_bytes, "big")

            # Read payload
            payload = b""
            while len(payload) < length:
                chunk = self.conn.recv(length - len(payload))
                if not chunk:
                    break
                payload += chunk

            # Deserialize
            data = pickle.loads(payload)
            buffer = data["frame"]
            
            # Convert buffer back into an image
            frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

            if frame is None:
                print("Failed to decode frame")
                continue

            # --- FPS calculation ---
            self.frame_count += 1
            current_time = time.time()
            elapsed = current_time - self.prev_time
            if elapsed >= 1.0:  # update every second
                self.fps = self.frame_count / elapsed
                self.frame_count = 0
                self.prev_time = current_time

            # --- Overlay FPS and quit text ---
            cv2.putText(frame, f"FPS: {self.fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press Q to quit", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            # Show frame
            cv2.imshow("CPU Live Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.conn.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    receiver = CameraReceiver(host="0.0.0.0", port=5000)
    receiver.receive_data()
