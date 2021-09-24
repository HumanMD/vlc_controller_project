import threading


class VideoLanThread(threading.Thread):
    def __init__(self, action, parameters):
        threading.Thread.__init__(self)
        self.action = action
        self.parameters = parameters

    def run(self):
        print(f"{self.action}\n{self.parameters}")
