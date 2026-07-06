import time

class AutoCapture:
    def __init__(self):
        self.start_time = None
        self.required_duration = 1.0  

    def should_capture(self, score):
        if score >= 90:
            if self.start_time is None:
                self.start_time = time.time()  
            if time.time() - self.start_time >= self.required_duration:
                self.start_time = None 
                return True
        else:
            self.start_time = None

        return False