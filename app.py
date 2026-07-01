import cv2
from score.pose_score import PoseScorer
from camera.manager import CameraManager
from pose.detector import PoseDetector
from face.face_mesh import FaceMeshDetector
from face.analyzer import FaceAnalyzer
from recommendations.coach import PoseCoach
from pose.analyzer import PoseAnalyzer

pose_analyzer = PoseAnalyzer()
camera = CameraManager()
face_analyzer = FaceAnalyzer()
pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
pose_scorer = PoseScorer()
coach = PoseCoach()

mirror = True

while True:
    frame, fps = camera.read()
    if frame is None:
        break
    if mirror:
        frame = cv2.flip(frame, 1)
    frame, pose_results = pose_detector.detect(frame)
    frame, face_results = face_detector.detect(frame)

    pose_status = "Detected" if pose_results.pose_landmarks else "Not Detected"
    face_status = "Not Detected"

    eyes_status = "--"
    head_status = "--"
    smile_status = "--"
    suggestion = "--"
    if pose_results.pose_landmarks:

        pose_analysis = pose_analyzer.analyze(

            pose_results.pose_landmarks.landmark

        )
    if face_results.multi_face_landmarks:
        face_status = "Detected"  
        landmarks = face_results.multi_face_landmarks[0].landmark
        analysis = face_analyzer.analyze(landmarks)

        eyes_status = "Open" if analysis["eyes_open"] else "Closed"
        smile_status = "Yes 😊" if analysis["smile"] else "No"
        head_status = analysis["head"]
        
        # Duplicate line aur variable hata kar seedhe suggestion li
        suggestion = coach.get_suggestion(analysis)
        pose_score = pose_scorer.calculate_score(

            analysis,

            pose_results.pose_landmarks is not None

        )
    if fps >= 25:
        fps_color = (0, 255, 0)
    elif fps >= 15:
        fps_color = (0, 255, 255)
    else:
        fps_color = (0, 0, 255)

    # Pose & Face Colors
    pose_color = (0, 255, 0) if pose_status == "Detected" else (0, 0, 255)
    face_color = (0, 255, 0) if face_status == "Detected" else (0, 0, 255)
    eye_color = (0, 255, 0) if eyes_status == "Open" else (0, 0, 255)
    smile_color = (0, 255, 0) if smile_status == "Yes 😊" else (0, 0, 255)

#ui part
    cv2.putText(frame, 
                f"FPS : {fps}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, fps_color, 2)
    
    cv2.putText(frame,
                f"Pose : {pose_status}",
                (20, 80), 
                cv2.FONT_HERSHEY_SIMPLEX,
                 0.8, pose_color, 2)
    
    cv2.putText(frame, 
                f"Face : {face_status}",
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, face_color, 2)

    cv2.putText(frame, 
                f"Eyes : {eyes_status}", 
                (20, 160), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, eye_color, 2)

    
    cv2.putText(frame, 
                f"Head : {head_status}", 
                (20, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 255, 0), 2)
    
    mirror_status = "ON" if mirror else "OFF"
    cv2.putText(frame, 
                f"Mirror : {mirror_status}", 
                (20, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                (255, 255, 255), 2)
    
    
    cv2.putText(frame, 
                f"Suggestion: {suggestion}", 
                (20, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (0, 255, 255), 2)
    
    # 8. Smile (Y-coordinate fixed to 320)
    cv2.putText(frame, 
                f"Smile : {smile_status}",
                  (20, 320), 
                  cv2.FONT_HERSHEY_SIMPLEX, 
                  0.8, smile_color, 2)
    score_color = (
                (0,255,0)
                if pose_score >= 90
                else
                (0,255,255)
                if pose_score >= 70
                else
                (0,0,255)
            )

    cv2.putText(
                frame,
                f"Pose Score : {pose_score}/100",
                (20,360),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                score_color,
                2
            )
    # 9. Brand/Version Text
    cv2.putText(frame, "VisionPose AI v0.6", (830, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # --- Window and Keys ---
    cv2.imshow("AI Photography Assistant", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("m"):
        mirror = not mirror
    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()  # Windows ko clean karne ke liye close karna zaroori hai