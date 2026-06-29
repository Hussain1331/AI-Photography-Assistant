import cv2

from camera.manager import CameraManager
from pose.detector import PoseDetector
from face.face_mesh import FaceMeshDetector

camera = CameraManager()

pose_detector = PoseDetector()
face_detector = FaceMeshDetector()


while True:

    frame, fps = camera.read()

    if frame is None:
        break

    frame, pose_results = pose_detector.detect(frame)
    frame, face_results = face_detector.detect(frame)

    pose_status = "Detected" if pose_results.pose_landmarks else "Not Detected"

    face_status = (
        "Detected"
        if face_results.multi_face_landmarks
        else "Not Detected"
    )

    cv2.putText(
        frame,
        f"FPS : {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Pose : {pose_status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Face : {face_status}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    cv2.imshow("AI Photography Assistant", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()