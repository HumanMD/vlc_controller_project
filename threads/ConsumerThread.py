import threading
import time


class ConsumerThread(threading.Thread):
    def __init__(self, q_msg):
        threading.Thread.__init__(self)
        self.q_msg = q_msg

    def run(self):

        while True:
            time.sleep(2)
            msg = self.q_msg.get(True).split(',')
            print(f"consumer thread, consuming: {msg}")
