import os
import re
import signal
import sys
import threading


def regex_check(message):
    if re.findall("^(start|stop|focus+)(,)([1-4])$", message):
        return True


class ProducerThread(threading.Thread):
    def __init__(self, q_msg, conn):
        threading.Thread.__init__(self)
        self.q_msg = q_msg
        self.conn = conn

    def run(self):

        while True:
            data = self.conn.recv(4096)
            msg = str(data, 'utf-8')

            if msg == 'esc':
                print('closing connection')
                self.q_msg.put(msg, True)
                sys.exit()

            elif not regex_check(msg):
                print('illegal input! \n')
                continue

            self.q_msg.put(msg, True)
            print(f"producer thread, insert: {msg} \n")
