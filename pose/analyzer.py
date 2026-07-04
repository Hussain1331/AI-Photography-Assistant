import math

class PoseAnalyzer:
    def distance(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def calculate_angle(self, a, b, c):
        # b se a aur b se c ke beech ka angle nikalne ke liye
        ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
        res = abs(ang)
        return res if res <= 180 else 360 - res

    def analyze(self, landmarks):
        # MediaPipe Pose Landmarks IDs:
        # Left Arm: Shoulder(11), Elbow(13), Wrist(15)
        # Right Arm: Shoulder(12), Elbow(14), Wrist(16)
        # Left Leg: Hip(23), Knee(25), Ankle(27)
        # Right Leg: Hip(24), Knee(26), Ankle(28)
        
        l_shoulder = landmarks[11]
        r_shoulder = landmarks[12]
        
        l_elbow = landmarks[13]
        r_elbow = landmarks[14]
        l_wrist = landmarks[15]
        r_wrist = landmarks[16]

        l_hip = landmarks[23]
        r_hip = landmarks[24]
        l_knee = landmarks[25]
        r_knee = landmarks[26]
        l_ankle = landmarks[27]
        r_ankle = landmarks[28]

        # 1. Shoulder Level Calculation
        shoulder_diff = abs(l_shoulder.y - r_shoulder.y)
        shoulder_status = "Level" if shoulder_diff < 0.03 else "Not Level"

        # 2. Calculate Raw Angles (Arms)
        left_arm_angle = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
        right_arm_angle = self.calculate_angle(r_shoulder, r_elbow, r_wrist)

        # 3. Calculate Raw Angles (Legs - Fixed KeyError)
        left_leg_angle = self.calculate_angle(l_hip, l_knee, l_ankle)
        right_leg_angle = self.calculate_angle(r_hip, r_knee, r_ankle)

        # 4. Determine Status Strings
        left_arm_status = "Straight" if left_arm_angle > 150 else "Relaxed"
        right_arm_status = "Straight" if right_arm_angle > 150 else "Relaxed"

        # Saare variables dictionary mein pack karke bhej rahe hain taaki Matcher crash na ho
        return {
            "shoulder": shoulder_status,
            "left_arm": left_arm_status,
            "right_arm": right_arm_status,
            "left_arm_angle": left_arm_angle,
            "right_arm_angle": right_arm_angle,
            "left_leg_angle": left_leg_angle,    # <-- Matcher line 50 crash fixed!
            "right_leg_angle": right_leg_angle,  # <-- Matcher safe check path
            "shoulder_diff": shoulder_diff
        }