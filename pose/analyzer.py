from pose.angles import AngleCalculator


class PoseAnalyzer:

    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15

    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16

    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27

    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28

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
        left_leg = self.angle.calculate(
            landmarks[self.LEFT_HIP],
            landmarks[self.LEFT_KNEE],
            landmarks[self.LEFT_ANKLE]
        )

        right_leg = self.angle.calculate(
            landmarks[self.RIGHT_HIP],
            landmarks[self.RIGHT_KNEE],
            landmarks[self.RIGHT_ANKLE]
        )
        left_leg_status = (
            "Straight"
            if left_leg > 160
            else "Bent"
        )

        right_leg_status = (
            "Straight"
            if right_leg > 160
            else "Bent"
        )
        left_shoulder = landmarks[self.LEFT_SHOULDER]
        right_shoulder = landmarks[self.RIGHT_SHOULDER]

        difference = left_shoulder.y - right_shoulder.y

        if abs(difference) < 0.03:
            shoulder = "Level"

        elif difference > 0:
            shoulder = "Tilted Left"

        else:
            shoulder = "Tilted Right"
        return {
            "left_arm_angle": left_arm,
            "right_arm_angle": right_arm,

            "left_arm": left_arm_status,
            "right_arm": right_arm_status,

            "left_leg_angle": left_leg,
            "right_leg_angle": right_leg,

            "left_leg": left_leg_status,
            "right_leg": right_leg_status,
            "shoulder": shoulder
        }