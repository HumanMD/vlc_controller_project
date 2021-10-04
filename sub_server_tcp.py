import os
import queue
import re
import socket
import sys
import threading
import time
import tkinter as tk
import vlc
from screeninfo import get_monitors
from Producer import ProducerThread
from Window import Window

HOST = ""
PORT = 15000
q = queue.Queue(maxsize=4)
lock = threading.Lock()
initial = ''

# GET PRIMARY MONITOR DIMENSION AND DEFINE THE WINDOWS DIMENSION AND POSITION BASED ON IT
monitor = get_monitors()[0]
root = tk.Tk()
root.withdraw()  # hide the root so that only the video lan windows will be visible
w = int(monitor.width / 4)
h = int(monitor.height / 4)
ml = int(w - monitor.width / 16)  # base margin left
mt = int(h - monitor.height / 12)  # base margin top
dimension = str(w) + 'x' + str(h) + '+'

current_state = [
    dict(vl_number=1, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(monitor.x) + '+' + str(monitor.y)),
    dict(vl_number=2, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(ml) + '+' + str(mt)),
    dict(vl_number=3, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(2 * ml) + '+' + str(2 * mt)),
    dict(vl_number=4, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(3 * ml) + '+' + str(3 * mt))
]  # STATE VECTOR TO TAKE TRACK OF CHANGES MADE BY VLC-THREADS
new_msg = dict(vl=0, action=initial)  # LAST MESSAGE WROTE BY CONSUMER


# DEFINE THE VLC INSTANCE, THE WINDOW TO DISPLAY IT, AND UPDATE THE STATE OF THE VIDEO-LAN
def create_window(vl_number, root_window, state, new_action):
    i = vlc.Instance('--no-xlib --quiet')
    new_vl_instance = i.media_player_new()
    new_vl_instance.set_mrl("video" + str(vl_number) + ".mp4")
    new_window = Window(root_window, 'Video Lan ' + str(vl_number), new_vl_instance, state['w_h_x_y'])
    new_vl_instance.play()

    state.update(
        {'action': new_action, 'vl_instance': new_vl_instance, 'window': new_window})


# DESTROY THE WINDOW AND STOP VLC_INSTANCE PRESENT IN STATE
def destroy_window(state):
    state['window'].destroy()
    state['vl_instance'].stop()


class ConsumerThread(threading.Thread):
    def __init__(self, q_msg):
        threading.Thread.__init__(self)
        self.q_msg = q_msg

    def run(self):
        global new_msg

        while True:
            time.sleep(0.5)
            array_msg = self.q_msg.get(True).split(',')
            new_msg.update({
                'vl': int(array_msg[1]),
                'action': array_msg[0]
            })
            print(f"consumer thread, consuming: {new_msg}... ")


class VideoLanThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global lock
        global current_state
        global new_msg
        while True:
            lock.acquire()
            vl = new_msg['vl']

            if vl != 0:  # action != ''
                state = current_state[vl - 1]
                new_action = new_msg['action']
                current_action = state['action']
                current_vl_instance = state['vl_instance']

                if new_action == 'start':
                    print(f"{self.name}: {new_action} vl {vl}")
                    os.chdir("/home/human/Video")

                    if current_vl_instance == '':
                        create_window(vl, root, state, new_action)

                    else:
                        destroy_window(state)
                        time.sleep(0.2)
                        create_window(vl, root, state, new_action)

                elif new_action == 'stop' and \
                        new_action != current_action and \
                        current_vl_instance != '':
                    print(f"{self.name}: {new_action} vl {vl}")
                    destroy_window(state)

                new_msg.update({
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

    root.mainloop()


if __name__ == "__main__":
    sub_server((HOST, PORT))
