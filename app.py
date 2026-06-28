import cv2
import time
from pose.detector import PoseDetector
from pose.detector import PoseDetector

detector = PoseDetector()

cap = cv2.VideoCapture(0)

prev_time = 0

while True:
    success, frame = cap.read()
    frame, results = detector.detect(frame)
    if results.pose_landmarks:
        total = len(results.pose_landmarks.landmark)

        cv2.putText(
            frame,
            f"Landmarks: {total}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )
    if not success:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time else 0
    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("AI Photography Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()