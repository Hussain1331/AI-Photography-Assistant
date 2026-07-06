from ultralytics import YOLO
import cv2
class SceneAnalyzer:
    def __init__(self):
        self.model = YOLO("yolov8n.pt") 
    def analyze_scene(self, frame):
        results = self.model(frame, verbose=False)[0]
        detected_objects = []
        for box in results.boxes:
            class_id = int(box.cls[0])
            label = self.model.names[class_id]
            detected_objects.append(label)  
        if "chair" in detected_objects or "couch" in detected_objects:
            return "Sitting/Cafe Vibe", "Mujhe aas-paas chair/couch dikh rahi hai. Sitting aesthetic pose try kijiye!"  
        elif "potted plant" in detected_objects or "nature" in detected_objects:
            return "Nature/Outdoor", "Greenery waala background hai! Casual candid ya walking pose badhiya lagega."
            return "Cozy Indoor/Bedroom", "Cozy indoor setup hai. Relaxed ya leaning pose try karein."
        return "Standard Studio/Wall", "Simple background hai. Confident standing ya wall-support pose try karein."