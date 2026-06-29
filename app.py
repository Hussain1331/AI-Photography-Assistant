import cv2

from camera.manager import CameraManager
from pose.detector import PoseDetector
from face.face_mesh import FaceMeshDetector
from face.analyzer import FaceAnalyzer
from recommendations.coach import PoseCoach


camera = CameraManager()
face_analyzer = FaceAnalyzer()
pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
coach = PoseCoach()

while True:

    frame, fps = camera.read()

    if frame is None:
        break

    frame, pose_results = pose_detector.detect(frame)
    frame, face_results = face_detector.detect(frame)

    pose_status = "Detected" if pose_results.pose_landmarks else "Not Detected"
    face_status = "Not Detected"

    eyes_status = "--"
    head_status = "--"
    smile_status = "--"
    suggestion = "--"

    if face_results.multi_face_landmarks:

        face_status = "Detected"

        landmarks = (
            face_results
            .multi_face_landmarks[0]
            .landmark
        )

        analysis = face_analyzer.analyze(landmarks)

        eyes_status = (
            "Open"
            if analysis["eyes_open"]
            else "Closed"
        )
        smile_status = (
        "Yes 😊"
        if analysis["smile"]
        else "No"
        )

        head_status = analysis["head"]
        analysis = face_analyzer.analyze(landmarks)
        suggestion = coach.get_suggestion(analysis)#last changed here

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

    

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    cv2.putText(
        frame,
        f"Eyes : {eyes_status}",
        (20,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )
    cv2.putText(
        frame,
        f"Head : {head_status}",
        (20,200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )
    cv2.putText(
    frame,
    f"Suggestion: {suggestion}",
    (20, 240),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 255),
    2,
)
    cv2.putText(
        frame,
        f"Smile : {smile_status}",
        (20, 280),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 255),
        2,
    )
    cv2.imshow("AI Photography Assistant", frame)
camera.release()

