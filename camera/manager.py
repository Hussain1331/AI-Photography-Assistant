import cv2
import time


class CameraManager:

    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture(camera_index)
        self.prev_time = 0

    def read(self):

        success, frame = self.cap.read()

        if not success:
            return None, None

        current_time = time.time()

        fps = 1 / (current_time - self.prev_time) if self.prev_time else 0

        self.prev_time = current_time

        return frame, int(fps)

    def release(self):

        self.cap.release()
        cv2.destroyAllWindows()