from pose.angles import AngleCalculator


class PoseAnalyzer:

    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15

    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16

    def __init__(self):
        self.angle = AngleCalculator()

    def analyze(self, landmarks):

        left_arm = self.angle.calculate(
            landmarks[self.LEFT_SHOULDER],
            landmarks[self.LEFT_ELBOW],
            landmarks[self.LEFT_WRIST]
        )

        right_arm = self.angle.calculate(
            landmarks[self.RIGHT_SHOULDER],
            landmarks[self.RIGHT_ELBOW],
            landmarks[self.RIGHT_WRIST]
        )
        left_arm_status = (
            "Straight"
            if left_arm > 160
            else "Bent"
        )

        right_arm_status = (
            "Straight"
            if right_arm > 160
            else "Bent"
        )

        return {
            "left_arm_angle": left_arm,
            "right_arm_angle": right_arm,
            "left_arm_status": left_arm_status,
            "right_arm_status": right_arm_status
        }