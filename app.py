import time
import cv2
from score.pose_score import PoseScorer
from camera.manager import CameraManager
from pose.detector import PoseDetector
from face.face_mesh import FaceMeshDetector
from face.analyzer import FaceAnalyzer
from recommendations.coach import PoseCoach
from pose.analyzer import PoseAnalyzer
from recommendations.pose_matcher import PoseMatcher
from recommendations.pose_recommender import PoseRecommender
from recommendations.pose_stabilizer import PoseStabilizer
from capture.auto_capture import AutoCapture
from recommendations.ghost_guide import GhostGuide


# Initialize models
pose_analyzer = PoseAnalyzer()
camera = CameraManager()
face_analyzer = FaceAnalyzer()
pose_detector = PoseDetector()
face_detector = FaceMeshDetector()
pose_scorer = PoseScorer()
coach = PoseCoach()
matcher = PoseMatcher()
recommender = PoseRecommender()
stabilizer = PoseStabilizer(history_size=10)
auto_capture = AutoCapture()
ghost_guide = GhostGuide()
mirror = True

while True:
    frame, fps = camera.read()
    if frame is None:
        break
        
    if mirror:
        frame = cv2.flip(frame, 1)
        
    # Detectors
    frame, pose_results = pose_detector.detect(frame)
    frame, face_results = face_detector.detect(frame)

    pose_status = "Detected" if pose_results.pose_landmarks else "Not Detected"
    face_status = "Detected" if face_results.multi_face_landmarks else "Not Detected"

    eyes_status = "--"
    head_status = "--"
    smile_status = "--"
    suggestion = "--"
    pose_suggestion = "--"
    current_pose = "--"
    shoulder_status = "--"
    match_score = 0
    pose_score = 0
    recommended = ["No Recommendation"]  # Default list fallback

    # --- 1. Pose Processing ---
    pose_detected = pose_results.pose_landmarks is not None
    if pose_detected:
        pose_analysis = pose_analyzer.analyze(pose_results.pose_landmarks.landmark)
        shoulder_status = pose_analysis["shoulder"]
        pose_suggestion = coach.get_pose_suggestion(pose_analysis)
        
        match = matcher.compare(pose_analysis)
        match_score = match["score"]
        
        current_pose = stabilizer.update(match["pose"])
        recommended = recommender.recommend(current_pose)

        print(pose_analysis)
        print(match)
        print(pose_suggestion)
   
    # --- 2. Face Processing ---
    face_analysis_data = {"eyes_open": False, "smile": False, "head": "Unknown"}

    if face_results.multi_face_landmarks:
        landmarks = face_results.multi_face_landmarks[0].landmark
        analysis = face_analyzer.analyze(landmarks)
        face_analysis_data = analysis  # real data saved

        eyes_status = "Open" if analysis["eyes_open"] else "Closed"
        smile_status = "Yes" if analysis["smile"] else "No"
        head_status = analysis["head"]
        
        suggestion = coach.get_suggestion(analysis)

    # --- 3. Scoring & Auto Capture ---
    pose_score = pose_scorer.calculate_score(face_analysis_data, pose_detected)

    if auto_capture.should_capture(pose_score):
        print("!!! AUTO CAPTURE TRIGGERED !!!")
        
        
        import os
        if not os.path.exists("captures"):
            os.makedirs("captures")
            print("Created 'captures/' directory automatically!")

        filename = f"captures/photo_{int(time.time())}.jpg"
        success = cv2.imwrite(filename, frame)
        print(f"Photo Save Status: {success} | Saved as: {filename}")
    # --- 4. UI Colors Setup ---
    if fps >= 25:
        fps_color = (0, 255, 0)
    elif fps >= 15:
        fps_color = (0, 255, 255)
    else:
        fps_color = (0, 0, 255)

    pose_color = (0, 255, 0) if pose_status == "Detected" else (0, 0, 255)
    face_color = (0, 255, 0) if face_status == "Detected" else (0, 0, 255)
    eye_color = (0, 255, 0) if eyes_status == "Open" else (0, 0, 255)
    smile_color = (0, 255, 0) if smile_status == "Yes 😊" else (0, 0, 255)

    score_color = (0, 255, 0) if pose_score >= 90 else (0, 255, 255) if pose_score >= 70 else (0, 0, 255)

    # --- 5. Drawing UI ---
    cv2.putText(frame, f"FPS : {fps}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, fps_color, 2)
    cv2.putText(frame, f"Pose : {pose_status}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, pose_color, 2)
    cv2.putText(frame, f"Face : {face_status}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, face_color, 2)
    cv2.putText(frame, f"Eyes : {eyes_status}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, eye_color, 2)
    cv2.putText(frame, f"Head : {head_status}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    mirror_status = "ON" if mirror else "OFF"
    cv2.putText(frame, f"Mirror : {mirror_status}", (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"Suggestion: {suggestion}", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Smile : {smile_status}", (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.8, smile_color, 2)
    cv2.putText(frame, f"Pose Score : {pose_score}/100", (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, score_color, 2)
    cv2.putText(frame, f"Shoulders : {shoulder_status}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
    # Safe check for recommendation list
    next_pose_text = recommended[0] if recommended else "--"
    cv2.putText(frame, f"Next Pose : {next_pose_text}", (20, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    cv2.putText(frame, "VisionPose AI v0.6", (830, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "Recommended:", (20, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    for i, pose in enumerate(recommended):
        cv2.putText(frame, f"{i+1}. {pose}", (40, 520 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # Target suggestion pass karke skeleton framework screen par guide overlay karega
    frame = ghost_guide.draw_guide(frame, recommended[0])

    # --- Window and Keys ---
    cv2.imshow("AI Photography Assistant", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("m"):
        mirror = not mirror
    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()