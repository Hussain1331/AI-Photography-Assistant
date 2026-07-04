from collections import Counter


class PoseStabilizer:

    def __init__(self, history_size=10):

        self.history = []
        self.history_size = history_size

    def update(self, pose):

        self.history.append(pose)

        if len(self.history) > self.history_size:
            self.history.pop(0)

        return Counter(self.history).most_common(1)[0][0]