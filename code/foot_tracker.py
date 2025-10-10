import cv2
import numpy as np
import mediapipe as mp
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Low-light enhancement ---
def enhance_low_light(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_frame = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    denoised = cv2.bilateralFilter(enhanced_frame, d=9, sigmaColor=75, sigmaSpace=75)

    gamma = 1.2
    lut = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in range(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(denoised, lut)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(gamma_corrected, -1, kernel)

    return sharpened

# --- Kalman filter setup ---
def create_kalman_filter():
    kf = cv2.KalmanFilter(4, 2)
    kf.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)
    kf.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], dtype=np.float32)
    kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
    kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.5
    kf.errorCovPost = np.eye(4, dtype=np.float32)
    return kf

left_kf = create_kalman_filter()
right_kf = create_kalman_filter()

# --- MediaPipe Pose ---
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# --- Video input ---
cap = cv2.VideoCapture("assets/walking_video.mp4")

# --- CSV logging ---
csv_data = []
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    enhanced_frame = enhance_low_light(frame)
    rgb_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    left_pred = left_kf.predict()
    right_pred = right_kf.predict()

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w, _ = enhanced_frame.shape

        left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL]
        right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL]

        left_meas = np.array([[left_heel.x * w], [left_heel.y * h]], dtype=np.float32)
        right_meas = np.array([[right_heel.x * w], [right_heel.y * h]], dtype=np.float32)

        left_kf.correct(left_meas)
        right_kf.correct(right_meas)

    left_foot_pos = (int(left_pred[0]), int(left_pred[1]))
    right_foot_pos = (int(right_pred[0]), int(right_pred[1]))

    csv_data.append([frame_count, left_foot_pos[0], left_foot_pos[1], right_foot_pos[0], right_foot_pos[1]])

    cv2.circle(enhanced_frame, left_foot_pos, 5, (0, 255, 0), -1)
    cv2.circle(enhanced_frame, right_foot_pos, 5, (0, 0, 255), -1)

    cv2.imshow("Foot Tracking", enhanced_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

# --- Save to CSV ---
with open("data/foot_positions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "left_x", "left_y", "right_x", "right_y"])
    writer.writerows(csv_data)

# --- Animated Y vs X plot ---
csv_data = np.array(csv_data)
left_x = csv_data[:, 1]
left_y = csv_data[:, 2]
right_x = csv_data[:, 3]
right_y = csv_data[:, 4]

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, max(np.max(left_x), np.max(right_x)) + 50)
ax.set_ylim(0, max(np.max(left_y), np.max(right_y)) + 50)
ax.set_xlabel("Horizontal Position (X)")
ax.set_ylabel("Vertical Position (Y)")
ax.set_title("Foot Trajectories (Y vs X) Over Time")
ax.grid(True)

left_line, = ax.plot([], [], 'g-', label="Left Foot")
right_line, = ax.plot([], [], 'r-', label="Right Foot")
ax.legend()

def update(frame):
    left_line.set_data(left_x[:frame], left_y[:frame])
    right_line.set_data(right_x[:frame], right_y[:frame])
    return left_line, right_line

ani = animation.FuncAnimation(fig, update, frames=len(csv_data), interval=30, blit=True)
plt.tight_layout()
plt.show()
