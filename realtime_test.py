import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

from utils.detector import DrowsinessDetector
from utils.alarm import AlertManager


model_path = "face_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading MediaPipe model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
        model_path
    )
    print("Done!")


base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector   = vision.FaceLandmarker.create_from_options(options)
drowsy_det = DrowsinessDetector()
alert_mgr  = AlertManager()

# Eye and mouth indexes
LEFT_EYE  = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH     = [61, 291, 39, 181, 0, 17, 269, 405]

cap = cv2.VideoCapture(0)
print("DrowsyGuard running... Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    results  = detector.detect(mp_image)

    if results.face_landmarks:
        landmarks = results.face_landmarks[0]

        data = drowsy_det.update(landmarks, w, h)
        alert_mgr.update(data["alert_level"])

        color = alert_mgr.get_color(data["alert_level"])

    
        for idx in LEFT_EYE + RIGHT_EYE:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 2, color, -1)

       
        for idx in MOUTH:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 2, (255, 255, 0), -1)

        
        cv2.putText(frame, f"EAR: {data['ear']}",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"MAR: {data['mar']}",
                    (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Yawns: {data['yawn_count']}",
                    (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Frames: {data['frame_counter']}",
                    (30, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        
        cv2.putText(frame, data["status"],
                    (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

        
        border = alert_mgr.get_border_color(data["alert_level"])
        if border:
            cv2.rectangle(frame, (0, 0), (w, h), border, 5)

    else:
        cv2.putText(frame, "No Face Detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        alert_mgr.update(0)

    cv2.imshow("DrowsyGuard", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()