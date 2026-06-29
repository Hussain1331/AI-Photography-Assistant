import math
class FaceAnalyzer:

    # Left Eye
    LEFT_EYE = [33, 160, 158, 133, 153, 144]

    # Right Eye
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def distance(self, p1, p2):
        return math.hypot(
            p1.x - p2.x,
            p1.y - p2.y
        )

    def eye_aspect_ratio(self, landmarks, eye):

        p1 = landmarks[eye[0]]
        p2 = landmarks[eye[1]]
        p3 = landmarks[eye[2]]
        p4 = landmarks[eye[3]]
        p5 = landmarks[eye[4]]
        p6 = landmarks[eye[5]]

        vertical = (
            self.distance(p2, p6)
            + self.distance(p3, p5)
        )

        horizontal = (
            2 * self.distance(p1, p4)
        )

        return vertical / horizontal
    
    def head_direction(self, landmarks):

        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose = landmarks[1]

        left_dist = abs(nose.x - left_eye.x)
        right_dist = abs(right_eye.x - nose.x)

        diff = left_dist - right_dist

        if diff > 0.03:
            return "Left"

        elif diff < -0.03:
            return "Right"

        return "Straight"

    def analyze(self, landmarks):

        left = self.eye_aspect_ratio(
            landmarks,
            self.LEFT_EYE
        )

        right = self.eye_aspect_ratio(
            landmarks,
            self.RIGHT_EYE
        )

        ear = (left + right) / 2

        smile = self.smile_score(landmarks)

        return {

            "eyes_open": ear > 0.23,

            "ear": ear,

            "head": self.head_direction(landmarks),

            "smile": smile > 3.0,

            "smile_score": smile

        }
    
    def smile_score(self, landmarks):

        left = landmarks[61]
        right = landmarks[291]

        upper = landmarks[13]
        lower = landmarks[14]

        width = self.distance(left, right)
        height = self.distance(upper, lower)

        return width / height