import re
import sys
import threading


# COMPARE REGEX_CHECK AND CLASSIC_CHECK
# a = datetime.datetime.now()
# regex_check(msg)
# b = datetime.datetime.now()
# c = b-a
# print(c)
# print(f"total_seconds_delay: {c.total_seconds()}")
# print(f"second_delay: {c.seconds}")
# print(f"microsecond_delay: {c.microseconds}")


def regex_check(message):
    if re.findall("^(start|stop+)(,)([1-4])$", message):
        return True


def classic_check(message):
    messages = message.split(',')
    actions = ['start', 'stop']
    parameters = ['1', '2', '3', '4']

    if (len(messages) == 2) \
            and \
            (any(x == messages[0] for x in actions)) \
            and \
            (any(x == messages[1] for x in parameters)):
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
                sys.exit()

            if not regex_check(msg):
                print('illegal input!')
                continue

            self.q_msg.put(msg, True)
            print(f"producer thread, insert: {msg}")
