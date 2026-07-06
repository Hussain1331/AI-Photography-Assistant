import cv2

class GhostGuide:
    def __init__(self):
        
        self.connections = [
            (11, 12), # Shoulder to Shoulder
            (11, 13), (13, 15), # Left Arm (Shoulder-Elbow-Wrist)
            (12, 14), (14, 16), # Right Arm
            (11, 23), (12, 24), # Torso (Shoulder to Hip)
            (23, 24), # Hip to Hip
            (23, 25), (25, 27), # Left Leg (Hip-Knee-Ankle)
            (24, 26), (26, 28)  # Right Leg
        ]

    def draw_guide(self, frame, current_recommendation):
       
        h, w, _ = frame.shape
        color = (255, 255, 255) 
        thickness = 2
        cx, cy = w // 2, h // 2
        cv2.putText(frame, f"Align with Guide: {current_recommendation}", (cx - 150, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.rectangle(frame, (cx - 120, cy - 180), (cx + 120, cy + 220), (200, 200, 200), 1, cv2.LINE_AA)
        cv2.circle(frame, (cx, cy - 120), 40, (200, 200, 200), 1, cv2.LINE_AA) # Head guide
        
        return frame