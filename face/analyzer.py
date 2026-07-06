import math

class FaceAnalyzer:
    # Left & Right Eye MediaPipe Mesh IDs
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def distance(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def eye_aspect_ratio(self, landmarks, eye):
        p1, p2, p3, p4, p5, p6 = [landmarks[i] for i in eye]
        vertical = self.distance(p2, p6) + self.distance(p3, p5)
        horizontal = 2.0 * self.distance(p1, p4)
        return vertical / horizontal
    
    def head_direction(self, landmarks):
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose = landmarks[1]

        left_dist = abs(nose.x - left_eye.x)
        right_dist = abs(right_eye.x - nose.x)
        diff = left_dist - right_dist

        # Mirror mode compatible thresholds
        if diff > 0.04: return "Right"  # Flipped framework check
        if diff < -0.04: return "Left"
        return "Straight"

    def smile_score(self, landmarks):
        # Lips outer corners
        left_lip = landmarks[61]
        right_lip = landmarks[291]
        # Lips center vertical points
        upper_lip = landmarks[13]
        lower_lip = landmarks[14]

        width = self.distance(left_lip, right_lip)
        height = self.distance(upper_lip, lower_lip)
        
        if height == 0: return 0
        return width / height

    def analyze(self, landmarks):
        left_ear = self.eye_aspect_ratio(landmarks, self.LEFT_EYE)
        right_ear = self.eye_aspect_ratio(landmarks, self.RIGHT_EYE)
        ear = (left_ear + right_ear) / 2.0

        smile_ratio = self.smile_score(landmarks)

        is_smiling = smile_ratio > 4.2 or (smile_ratio < 2.2 and smile_ratio > 0)

        return {
            "eyes_open": ear > 0.20, # Calibrated standard threshold
            "ear": ear,
            "head": self.head_direction(landmarks),
            "smile": is_smiling,
            "smile_score": smile_ratio
        }