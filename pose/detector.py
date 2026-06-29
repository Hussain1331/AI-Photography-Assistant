import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(rgb)

        if results.pose_landmarks:

            self.drawer.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.drawer.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=2,
                    circle_radius=2,
                ),
                self.drawer.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2,
                    circle_radius=2,
                ),
            )

        return frame, results