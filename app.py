import streamlit as st
import cv2
import time
import os
import numpy as np

# Core Modules Import
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

# Page Configuration for Premium Wide Layout
st.set_page_config(page_title="VisionPose Studio Pro", layout="wide", page_icon="📸")

# --- 🎨 CUSTOM GLASSMORPHIC CSS INJECTION ---
st.markdown("""
    <style>
    /* Main Background Theme Tweak */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%);
        color: #f0f0f5;
    }
    
    /* Premium Glassmorphic Cards Styling */
    .premium-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Neon Status Indicators */
    .status-badge {
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .badge-green { background: rgba(0, 255, 136, 0.15); color: #00ff88; border: 1px solid #00ff88; }
    .badge-yellow { background: rgba(255, 187, 0, 0.15); color: #ffbb00; border: 1px solid #ffbb00; }
    .badge-red { background: rgba(255, 51, 51, 0.15); color: #ff3333; border: 1px solid #ff3333; }
    
    /* Photo Gallery Interactive Cards */
    .gallery-card {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        background: #191432;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .gallery-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #00ff88;
        box-shadow: 0 12px 25px rgba(0, 255, 136, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# App Branding
st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight: 800; letter-spacing: -1px;'>📸 VisionPose <span style='color: #00ff88;'>Studio Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0b8; margin-top: -10px;'>Next-Gen Context-Aware AI Photography & Cinematic Framing Suite</p>", unsafe_allow_html=True)
st.write("---")

# Session State Initialization
if "session_photos" not in st.session_state:
    st.session_state.session_photos = []

# Main Workspace Split
col1, col2 = st.columns([2.2, 1])

with col2:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color: #00ff88;'>⚙️ Control Center</h3>", unsafe_allow_html=True)
    mirror = st.checkbox("Mirror View (Selfie Mode)", value=True)
    show_guide = st.checkbox("Enable Ghost Silhouette Guide", value=True)
    
    if st.button("🧹 Reset Capture Session", type="primary", use_container_width=True):
        st.session_state.session_photos = []
        st.toast("Session Reset Complete!", icon="🗑️")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🌐 Environment Engine</h3>", unsafe_allow_html=True)
    env_badge_placeholder = st.empty()
    env_text_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>📊 AI Analytics Pipeline</h3>", unsafe_allow_html=True)
    pose_metric = st.empty()
    face_metric = st.empty()
    coach_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

with col1:
    st.markdown("<div class='premium-card' style='padding: 10px;'>", unsafe_allow_html=True)
    frame_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Backend Models Setup ---
@st.cache_resource
def init_models():
    return (
        PoseAnalyzer(), CameraManager(), FaceAnalyzer(), PoseDetector(),
        FaceMeshDetector(), PoseScorer(), PoseCoach(), PoseMatcher(),
        PoseRecommender(), PoseStabilizer(history_size=10), AutoCapture(), 
        GhostGuide(), SceneAnalyzer()
    )

pose_analyzer, camera, face_analyzer, pose_detector, face_detector, \
pose_scorer, coach, matcher, recommender, stabilizer, auto_capture, ghost_guide, scene_analyzer = init_models()

# --- Frame Processing Loop ---
while True:
    frame, fps = camera.read()
    if frame is None:
        st.error("Webcam input stream not found.")
        break
        
    if mirror:
        frame = cv2.flip(frame, 1)
        
    h, w, _ = frame.shape

    # AI Context Detection
    scene_category, scene_suggestion = scene_analyzer.analyze_scene(frame)
    
    # Landmark Processing
    frame, pose_results = pose_detector.detect(frame)
    frame, face_results = face_detector.detect(frame)

    pose_status = "ACTIVE" if pose_results.pose_landmarks else "SEARCHING"
    face_status = "ACTIVE" if face_results.multi_face_landmarks else "SEARCHING"
    eyes_status, head_status, smile_status = "--", "--", "--"
    suggestion = "Positioning user frame..."
    shoulder_status = "--"
    pose_score = 0
    recommended = ["Casual Standing"]
    current_pose = "Unknown"

    framing_alert = ""
    pose_detected = pose_results.pose_landmarks is not None
    if pose_detected:
        pose_analysis = pose_analyzer.analyze(pose_results.pose_landmarks.landmark)
        shoulder_status = pose_analysis["shoulder"]
        match = matcher.compare(pose_analysis, active_category=scene_category)
        current_pose = stabilizer.update(match["pose"])
        recommended = recommender.recommend(current_pose)
        
        # Center Boundary Protection
        nose_x = pose_results.pose_landmarks.landmark[0].x
        if nose_x < 0.25:
            framing_alert = "⚠️ SHIFT RIGHT -> CENTER"
        elif nose_x > 0.75:
            framing_alert = "⚠️ SHIFT LEFT -> CENTER"

    face_analysis_data = {"eyes_open": False, "smile": False, "head": "Unknown"}
    if face_results.multi_face_landmarks:
        landmarks = face_results.multi_face_landmarks[0].landmark
        analysis = face_analyzer.analyze(landmarks)
        face_analysis_data = analysis
        eyes_status = "Open" if analysis["eyes_open"] else "Closed"
        smile_status = "Smiling" if analysis["smile"] else "Neutral"
        head_status = analysis["head"]
        suggestion = coach.get_suggestion(analysis)
        
        if framing_alert:
            suggestion = "Adjust framework position immediately."
            coach.speak("Please center yourself")

    # Score Evaluation & Intelligent Shutter Trigger
    pose_score = pose_scorer.calculate_score(face_analysis_data, pose_detected)
    
    if auto_capture.should_capture(pose_score):
        if not os.path.exists("captures"):
            os.makedirs("captures")
        img_name = f"captures/pro_shot_{int(time.time())}.jpg"
        cv2.imwrite(img_name, frame)
        st.session_state.session_photos.append({"path": img_name, "score": pose_score, "pose": current_pose})
        st.toast(f"💎 Masterpiece Captured! Score: {pose_score}", icon="🔥")
                
    if show_guide:
        frame = ghost_guide.draw_guide(frame, recommended[0])

    # Dynamic HUD Styling on Camera Matrix
    score_color = (0, 255, 136) if pose_score >= 90 else (0, 187, 255) if pose_score >= 70 else (51, 51, 255)
    cv2.rectangle(frame, (15, 15), (260, 105), (20, 16, 38), -1)
    cv2.rectangle(frame, (15, 15), (260, 105), (100, 100, 150), 1)
    cv2.putText(frame, f"AI MATCH: {pose_score}%", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, score_color, 2)
    cv2.putText(frame, f"TARGET: {recommended[0]}", (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 200), 1)

    if framing_alert:
        cv2.putText(frame, framing_alert, (w // 2 - 160, h - 50), cv2.FONT_HERSHEY_DUPLEX, 0.6, (51, 51, 255), 2)

    # Push Clean Frame to Display Array
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

    # --- Live Injecting Custom Styled Dashboard HTML Components ---
    env_badge_placeholder.markdown(f"<span class='status-badge badge-yellow'>⚡ {scene_category}</span>", unsafe_allow_html=True)
    env_text_placeholder.markdown(f"<p style='color:#a0a0b8; font-size:0.9rem; margin-top:10px;'>{scene_suggestion}</p>", unsafe_allow_html=True)
    
    pose_class = "badge-green" if pose_status == "ACTIVE" else "badge-red"
    face_class = "badge-green" if face_status == "ACTIVE" else "badge-red"
    
    pose_metric.markdown(f"<p style='margin-bottom:2px; color:#80809a;'>Body Tracker State</p><h4><span class='status-badge {pose_class}'>{pose_status}</span> <span style='font-size:1.1rem; color:#fff;'>| {current_pose}</span></h4>", unsafe_allow_html=True)
    face_metric.markdown(f"<p style='margin-bottom:2px; color:#80809a; margin-top:15px;'>Facial Analytics</p><h4><span class='status-badge {face_class}'>{face_status}</span> <span style='font-size:0.95rem; color:#a0a0b8;'>| {smile_status} ({head_status} Head)</span></h4>", unsafe_allow_html=True)
    
    coach_placeholder.markdown(f"<div style='background:rgba(0,255,136,0.06); padding:12px; border-radius:8px; border-left:4px solid #00ff88; margin-top:15px; color:#e0e0ed;'>🎙️ <b>AI Director:</b> {suggestion}</div>", unsafe_allow_html=True)

    # --- Render Aesthetic Premium Grid Gallery ---
    if st.session_state.session_photos:
        st.markdown("<br><h3>🎞️ Professional Session Masterpieces</h3>", unsafe_allow_html=True)
        latest_captures = st.session_state.session_photos[::-1][:4]
        g_cols = st.columns(4)
        
        for idx, shot in enumerate(latest_captures):
            with g_cols[idx]:
                if os.path.exists(shot["path"]):
                    score_class = "badge-green" if shot["score"] >= 90 else "badge-yellow" if shot["score"] >= 70 else "badge-red"
                    # HTML and Streamlit component nesting for high-end look
                    st.markdown(f"""
                        <div class='gallery-card'>
                            <div style='padding:10px 15px; display:flex; justify-content:space-between; align-items:center; background:#211b41;'>
                                <span style='font-size:0.85rem; font-weight:600; color:#fff;'>{shot['pose']}</span>
                                <span class='status-badge {score_class}' style='font-size:0.7rem; padding:2px 8px;'>{shot['score']}%</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.image(shot["path"], use_container_width=True)

    time.sleep(0.01)