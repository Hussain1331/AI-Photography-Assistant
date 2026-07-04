import json
import os

class PoseMatcher:

    def __init__(self):
        self.poses = []
        pose_folder = "poses"

        # 📂 Folder automatic banane ke liye agar nahi hai toh
        if not os.path.exists(pose_folder):
            os.makedirs(pose_folder)

        for file in os.listdir(pose_folder):
            if file.endswith(".json"):
                with open(os.path.join(pose_folder, file), "r") as f:
                    self.poses.append(json.load(f))

    def compare(self, pose_analysis):
        # 1. Safe Fallback: Agar database mein koi pose hi nahi hai
        if not self.poses:
            return {
                "pose": "No Pose Loaded",
                "score": 0
            }

        best_pose = None
        best_difference = float("inf")

        for pose in self.poses:
            difference = (
                abs(pose_analysis["left_arm_angle"] - pose.get("left_arm_angle", 180))
                + abs(pose_analysis["right_arm_angle"] - pose.get("right_arm_angle", 180))
                + abs(pose_analysis["left_leg_angle"] - pose.get("left_leg_angle", 180))
                + abs(pose_analysis["right_leg_angle"] - pose.get("right_leg_angle", 180))
            )
            
            if difference < best_difference:
                best_difference = difference
                best_pose = pose

        # 2. Score calculation
        score = max(0, 100 - int(best_difference / 2))

        # Safe dictionary access
        pose_name = best_pose["name"] if best_pose else "Unknown Pose"

        return {
            "pose": pose_name,
            "score": score
        }