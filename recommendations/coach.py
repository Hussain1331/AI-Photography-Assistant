class PoseCoach:

    def get_suggestion(self, analysis):

        if not analysis["eyes_open"]:
            return "Open your eyes"

        if analysis["head"] != "Straight":
            return "Look at the camera"
        if not analysis["eyes_open"]:

            suggestion = "Open your eyes"

        elif analysis["head"] != "Straight":

            suggestion = "Look at the camera"

        elif not analysis["smile"]:

            suggestion = "Try smiling 😊"

        else:

            suggestion = "Perfect! Hold Still 📸"

        return "Perfect! Hold Still"

    def get_pose_suggestion(self, pose_analysis):

        if pose_analysis["left_arm_status"] == "Straight":
            return "Relax your left arm"

        if pose_analysis["right_arm_status"] == "Straight":
            return "Relax your right arm"

        return "Good upper body pose"