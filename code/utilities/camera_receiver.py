import socket
import pickle
import cv2
import numpy as np
import time
from importlib import import_module
main = import_module("__main__")

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

        self.camera_visible = False
        self.is_camera_running = False
        self.received_data_frame = None

    def receive_data(self):
        while True:
            self.is_camera_running = True
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

            self.received_data_frame = frame

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

            if self.camera_visible:
                # --- Overlay FPS and quit text ---
                cv2.putText(frame, f"FPS: {self.fps:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Press Q to quit", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                # Show frame
                cv2.imshow("CPU Live Feed", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                cv2.destroyAllWindows()
                
        self.cleanup()

    def return_frame_data(self):
        return self.received_data_frame
    
    def show_new_frame(self, name, frame):
        if frame is not None:
            #self.camera_visible = True
            cv2.imshow(name, frame)
            cv2.waitKey(1)
        else:
            print("No frame data to show.")

    def show_filtered_feed(self):
        self.wall_lower_hsv = np.array([0, 0, 0])
        self.wall_upper_hsv = np.array([178, 255, 255])

        self.ball_lower_hsv = np.array([0, 0, 0])
        self.ball_upper_hsv = np.array([178, 255, 255])

        while True:
            self.is_camera_running = True
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

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            wall_mask = cv2.inRange(hsv, self.wall_lower_hsv, self.wall_upper_hsv)
            wall_result = cv2.bitwise_and(frame, frame, mask=wall_mask)

            ball_mask = cv2.inRange(hsv, self.ball_lower_hsv, self.ball_upper_hsv)
            ball_result = cv2.bitwise_and(frame, frame, mask=ball_mask)

            self.received_data_frame = frame

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

            if self.camera_visible:
                # --- Overlay FPS and quit text ---
                cv2.putText(frame, f"FPS: {self.fps:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Press Q to quit", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                # Resize frames
                display_w = 400
                display_h = 300

                raw_resized   = cv2.resize(frame,  (display_w, display_h))
                filt1_resized = cv2.resize(wall_result, (display_w, display_h))
                filt2_resized = cv2.resize(ball_result,   (display_w, display_h))

                # Black filler under raw frame
                black_resized = np.zeros((display_h, display_w, 3), dtype=np.uint8)

                # Build 2×2 grid
                top    = np.hstack((raw_resized, filt1_resized))
                bottom = np.hstack((black_resized, filt2_resized))

                combined = np.vstack((top, bottom))

                cv2.imshow("Combined Feed", combined)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                cv2.destroyAllWindows()
                
        self.cleanup()

    def get_filtered_frame(self, frame, mask):
        mask = np.array(mask)
        mask_frame = cv2.inRange(frame, mask[0], mask[1])
        filtered_frame = cv2.bitwise_and(frame, frame, mask=mask_frame)

        return filtered_frame
    
    def cleanup(self):
        self.conn.close()
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    receiver = CameraReceiver(host="0.0.0.0", port=5000)
    receiver.receive_data()
