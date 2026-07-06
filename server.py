from flask import Flask, render_template, Response, jsonify
import cv2
import os
import time

# Core Modules Import (Aapke existing components)
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
from recommendations.scene_analyzer import SceneAnalyzer

app = Flask(__name__)

# Global instances initialize kar rahe hain
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
scene_analyzer = SceneAnalyzer()
current_metrics = {
    "pose_score": 0,
    "current_pose": "Scanning",
    "scene_category": "Standard",
    "scene_suggestion": "Analyzing background...",
    "coach_suggestion": "Positioning...",
    "framing_alert": ""
}

def generate_frames():
    while True:
        frame, fps = camera.read()
        if frame is None:
            break
        # Standard processing
        frame = cv2.flip(frame, 1) # Selfie mirror mode default
        h, w, _ = frame.shape

        scene_category, scene_suggestion = scene_analyzer.analyze_scene(frame)
        
        # 2. Track Poses and Faces
        frame, pose_results = pose_detector.detect(frame)
        frame, face_results = face_detector.detect(frame)
        
        pose_detected = pose_results.pose_landmarks is not None
        current_pose = "Unknown"
        recommended = ["Casual Standing"]
        framing_alert = ""
        
        if pose_detected:
            pose_analysis = pose_analyzer.analyze(pose_results.pose_landmarks.landmark)
            match = matcher.compare(pose_analysis, active_category=scene_category)
            current_pose = stabilizer.update(match["pose"])
            recommended = recommender.recommend(current_pose)
            
            # Center Boundary Protection
            nose_x = pose_results.pose_landmarks.landmark[0].x
            if nose_x < 0.25: framing_alert = "⚠️ SHIFT RIGHT"
            elif nose_x > 0.75: framing_alert = "⚠️ SHIFT LEFT"

        face_analysis_data = {"eyes_open": False, "smile": False, "head": "Unknown"}
        suggestion = "Analyzing user framework..."
        if face_results.multi_face_landmarks:
            landmarks = face_results.multi_face_landmarks[0].landmark
            analysis = face_analyzer.analyze(landmarks)
            face_analysis_data = analysis
            suggestion = coach.get_suggestion(analysis)
            
            if framing_alert:
                suggestion = "Center yourself in the frame."
                coach.speak("Please center yourself")

        # 3. Final Evaluation
        pose_score = pose_scorer.calculate_score(face_analysis_data, pose_detected)
        
        if auto_capture.should_capture(pose_score):
            if not os.path.exists("static/captures"):
                os.makedirs("static/captures", exist_ok=True)
            img_name = f"static/captures/shot_{int(time.time())}.jpg"
            cv2.imwrite(img_name, frame)
            
        # 4. Ghost overlay draw karma
        frame = ghost_guide.draw_guide(frame, recommended[0])
        
        # Draw dynamic HUD on raw frame
        if framing_alert:
            cv2.putText(frame, framing_alert, (w // 2 - 100, h - 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

        # Update global dictionary for async AJAX/Fetch calls from UI
        global current_metrics
        current_metrics = {
            "pose_score": pose_score,
            "current_pose": current_pose,
            "scene_category": scene_category,
            "scene_suggestion": scene_suggestion,
            "coach_suggestion": suggestion,
            "framing_alert": framing_alert
        }

        # Compress and encode frame as JPEG bytes stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Stream endpoint mapping
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_metrics')
def get_metrics():
    # Asynchronous metrics channel
    return jsonify(current_metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5000)