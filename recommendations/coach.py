class PoseCoach:

    def get_suggestion(self, analysis):

            if not analysis["eyes_open"]:
                return "Open your eyes"

            elif analysis["head"] != "Straight":
                return "Look at the camera"

            elif not analysis["smile"]:
                return "Try smiling 😊"

            return "Perfect! Hold Still 📸"

    def get_pose_suggestion(self, pose_analysis):

        if pose_analysis["shoulder"] != "Level":
            return "Keep your shoulders level"

        if pose_analysis["left_arm"] == "Straight":
            return "Relax your left arm"

        if pose_analysis["right_arm"] == "Straight":
            return "Relax your right arm"

        return "Good upper body pose"