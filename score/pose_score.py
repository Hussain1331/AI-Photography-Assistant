class PoseScorer:

    def calculate_score(self, analysis, pose_detected):
        score = 0

        # 1. Pose Check (20 Points)
        if pose_detected:
            score += 20

        # 2. Eyes Status Check (30 Points)
        if analysis.get("eyes_open", False):
            score += 30

        # 3. Head Posture Check (30 Points)
        # Halka fulka left-right allowed hai, perfect target strict nahi rakhenge
        if analysis.get("head") == "Straight":
            score += 30
        elif analysis.get("head") in ["Left", "Right"]:
            score += 15 # Halka side face par bhi partial points de rahe hain

        # 4. Smile Check (20 Points)
        if analysis.get("smile", False):
            score += 20

        return score