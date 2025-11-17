import os
import cv2
import numpy as np

# --- Load Face Detector (Haar Cascade) ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# --- Load Object Detector (MobileNet SSD) ---
prototxt = "utilities/models/deploy.prototxt"   # Download from OpenCV repo
model = "utilities/models/res10_300x300_ssd_iter_140000.caffemodel"  # Pretrained weights

print("Prototxt exists:", os.path.exists(prototxt))
print("Model exists:", os.path.exists(model))

net = cv2.dnn.readNetFromCaffe(prototxt, model)

# --- Initialize Webcam ---
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]

    # --- Face Detection ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, fw, fh) in faces:
        cv2.rectangle(frame, (x, y), (x+fw, y+fh), (255, 0, 0), 2)
        cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # --- Object Detection (MobileNet SSD) ---
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 
                                 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # filter weak detections
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"Obj {confidence*100:.1f}%"
            cv2.putText(frame, text, (startX, startY-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # --- Show Output ---
    cv2.imshow("Face + Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
