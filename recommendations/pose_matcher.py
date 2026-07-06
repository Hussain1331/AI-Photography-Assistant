import json
import os

class PoseMatcher:
    def __init__(self):
        self.poses = []
        pose_folder = "poses"

        if not os.path.exists(pose_folder):
            os.makedirs(pose_folder)

        for file in os.listdir(pose_folder):
            if file.endswith(".json"):
                with open(os.path.join(pose_folder, file), "r") as f:
                    self.poses.append(json.load(f))

    def compare(self, pose_analysis, active_category="Standard Studio/Wall"):
        # 🎯 Filter poses based on AI detected background category
        filtered_poses = [p for p in self.poses if p.get("category", "Standard Studio/Wall") == active_category]
        
        # Fallback: Agar us category ka koi pose loaded nahi hai, toh saare poses check karo
        if not filtered_poses:
            filtered_poses = self.poses

        if not filtered_poses:
            return {"pose": "Casual Standing", "score": 0}

        best_pose = None
        best_difference = float("inf")

        for pose in filtered_poses:
            difference = (
                abs(pose_analysis["left_arm_angle"] - pose.get("left_arm_angle", 180))
                + abs(pose_analysis["right_arm_angle"] - pose.get("right_arm_angle", 180))
                + abs(pose_analysis["left_leg_angle"] - pose.get("left_leg_angle", 180))
                + abs(pose_analysis["right_leg_angle"] - pose.get("right_leg_angle", 180))
            )
            
            if difference < best_difference:
                best_difference = difference
                best_pose = pose

        score = max(0, 100 - int(best_difference / 2))
        pose_name = best_pose["name"] if best_pose else "Casual Standing"

        return {
            "pose": pose_name,
            "score": score
        }