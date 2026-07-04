import time

class AutoCapture:
    def __init__(self):
        self.start_time = None
        self.required_duration = 1.0  # 2 second se ghata kar 1 second kar diya (Practical hold time)

    def should_capture(self, score):
        if score >= 90:
            if self.start_time is None:
                self.start_time = time.time()  # Timer shuru

            # Agar lagatar 1 second tak 90+ score raha
            if time.time() - self.start_time >= self.required_duration:
                self.start_time = None  # Capture ke baad reset
                return True
        else:
            # Pura reset karne ki jagah thoda smooth exit:
            # Agar ek single frame drop hua toh direct None nahi karenge, 
            # par safety ke liye abhi simple rakhne ke liye instant reset hi sahi h agar score sach me bohot kam ho jaye.
            self.start_time = None

        return False