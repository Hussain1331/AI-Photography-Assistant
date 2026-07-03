import json
import os


class PoseMatcher:

    def __init__(self):

        self.poses = []

        pose_folder = "poses"

        for file in os.listdir(pose_folder):

            if file.endswith(".json"):

                with open(
                    os.path.join(pose_folder, file),
                    "r"
                ) as f:

                    self.poses.append(
                        json.load(f)
                    )

    def compare(self, pose_analysis):

        best_pose = None
        best_difference = float("inf")

        for pose in self.poses:

            difference = (

                abs(
                    pose_analysis["left_arm_angle"]
                    - pose["left_arm_angle"]
                )

                +

                abs(
                    pose_analysis["right_arm_angle"]
                    - pose["right_arm_angle"]
                )

                +

                abs(
                    pose_analysis["left_leg_angle"]
                    - pose["left_leg_angle"]
                )

                +

                abs(
                    pose_analysis["right_leg_angle"]
                    - pose["right_leg_angle"]
                )
            )
            if difference < best_difference:

                best_difference = difference
                best_pose = pose

        score = max(
            0,
            100 - int(best_difference / 2)
        )

        return {
            "pose": best_pose["name"],
            "score": score
        }