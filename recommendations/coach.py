import pyttsx3
import threading

class PoseCoach:
    def __init__(self):
       
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160) 
        self.last_speech_time = 0
        self.last_text = ""

    def _speak_worker(self, text):
        try:
           
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    def speak(self, text):
       
        if text != self.last_text:
            self.last_text = text
            threading.Thread(target=self._speak_worker, args=(text,), daemon=True).start()

    def get_suggestion(self, analysis):
        if not analysis["eyes_open"]:
            msg = "Open your eyes"
            self.speak(msg)
            return msg

        elif analysis["head"] != "Straight":
            msg = "Look at the camera"
            self.speak(msg)
            return msg

        elif not analysis["smile"]:
            msg = "Try smiling"
            self.speak(msg)
            return msg

        return "Perfect! Hold Still"
    def get_pose_suggestion(self, pose_analysis):
        if pose_analysis["shoulder"] != "Level":
            msg = "Keep your shoulders level"
            self.speak(msg)
            return msg
        if pose_analysis["left_arm"] == "Straight":
            msg = "Relax your left arm"
            self.speak(msg)
            return msg
        if pose_analysis["right_arm"] == "Straight":
            msg = "Relax your right arm"
            self.speak(msg)
            return msg

        self.speak("Good upper body pose, freeze!")
        return "Good upper body pose"