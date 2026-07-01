class PoseScorer:

    def calculate_score(
        self,
        analysis,
        pose_detected
    ):

        score = 0

        if pose_detected:
            score += 20

        if analysis["eyes_open"]:
            score += 30

        if analysis["head"] == "Straight":
            score += 30

        if analysis["smile"]:
            score += 20

        return score