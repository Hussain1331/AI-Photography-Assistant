class PoseRecommender:

    def recommend(self, current_pose):

        recommendations = {

            "Casual Standing": [
                "Hands In Pocket",
                "Crossed Arms",
                "Side Pose"
            ],

            "Hands In Pocket": [
                "Crossed Arms",
                "Looking Away",
                "Lean Pose"
            ],

            "Crossed Arms": [
                "Hands In Pocket",
                "Side Pose",
                "Confident Pose"
            ]
        }

        return recommendations.get(
            current_pose,
            ["Casual Standing"]
        )