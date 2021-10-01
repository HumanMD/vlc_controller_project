import os
import queue
import re
import socket
import sys
import threading
import time
import tkinter as tk
import vlc

from Producer import ProducerThread
from Window import Window

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=4)
lock = threading.Lock()
initial = ''
root = tk.Tk()

current_state = [
    dict(vl_number=1, vl_instance=initial, action=initial),
    dict(vl_number=2, vl_instance=initial, action=initial),
    dict(vl_number=3, vl_instance=initial, action=initial),
    dict(vl_number=3, vl_instance=initial, action=initial)
]
current_msg = dict(vl=0, action=initial)


class ConsumerThread(threading.Thread):
    def __init__(self, q_msg):
        threading.Thread.__init__(self)
        self.q_msg = q_msg

    def run(self):
        global current_msg

        while True:
            time.sleep(0.5)
            array_msg = self.q_msg.get(True).split(',')
            current_msg.update({
                'vl': int(array_msg[1]),
                'action': array_msg[0]
            })
            print(f"consumer thread, consuming: {current_msg}... ")


class VideoLanThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global lock
        global current_state
        global current_msg
        while True:
            lock.acquire()
            vl = current_msg['vl']

            if vl != 0:  # action != ''
                state = current_state[vl - 1]
                new_action = current_msg['action']
                current_action = state['action']
                current_vl_instance = state['vl_instance']

                if new_action == 'start':
                    print(f"{self.name}: {new_action} vl {vl}")
                    os.chdir("/home/human/Video")

                    if current_vl_instance == '':
                        i = vlc.Instance('--no-xlib --quiet')
                        new_vl_instance = i.media_player_new()
                        new_vl_instance.set_mrl("video" + str(vl) + ".mp4")
                        new_window = Window(root, vl, 'Video Lan ' + str(vl), new_vl_instance)
                        new_vl_instance.play()

                        state.update(
                            {'action': new_action, 'vl_instance': new_vl_instance})

                    else:
                        current_vl_instance.stop()
                        time.sleep(1)
                        current_vl_instance.play()

                elif new_action == 'stop' and \
                        new_action != current_action and \
                        current_vl_instance != '':
                    print(f"{self.name}: {new_action} vl {vl}")
                    current_vl_instance.stop()
                    state.update({'isRunning': False})

                current_msg.update({
                    'vl': 0,
                    'action': ''
                })

            lock.release()


def sub_server(address, backlog=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(backlog)
        print("server initialized, listening...")
    except socket.error as error:
        print(f"something wrong ...\n {error}")
        sys.exit()
    conn, client_address = s.accept()
    print(f"connection Server - Client established: {client_address} ")

    threads = [ProducerThread(q, conn), ConsumerThread(q),
               VideoLanThread('thread_1'), VideoLanThread('thread_2'),
               VideoLanThread('thread_3'), VideoLanThread('thread_4')]

    for thread in threads:
        thread.start()

    root.withdraw()  # hide the root so that only the video lan will be visible
    root.mainloop()


if __name__ == "__main__":
    sub_server((HOST, PORT))
