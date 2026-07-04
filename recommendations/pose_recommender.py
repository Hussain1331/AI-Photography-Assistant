import json
import os

class PoseRecommender:

    def __init__(self):
        self.database = {}
        folder = "poses"

        if not os.path.exists(folder):
            os.makedirs(folder)

        for file in os.listdir(folder):
            if file.endswith(".json"):
                with open(os.path.join(folder, file), "r") as f:
                    pose = json.load(f)
                    self.database[pose["name"]] = pose

    def recommend(self, current_pose):
        pose = self.database.get(current_pose)

        if pose is None:
            return ["Casual Standing"]

        next_poses = pose.get("next_pose", ["Casual Standing"])
        
        # Agar json mein "next_pose" sirf ek string h (e.g. "Hands in Pocket"), 
        # toh use list mein wrap kar rahe hain taaki UI loop crash na ho
        if isinstance(next_poses, str):
            return [next_poses]
            
        return next_poses