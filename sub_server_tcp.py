import os
import queue
import signal
import socket
import subprocess
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
monitor = get_monitors()[0]  # get the primary monitor instance
root = tk.Tk()  # instantiate the root window, where the vl-windows ll be played
root.withdraw()  # hide the root so that only the vl-windows will be visible

# TODO let the client able to specify the dimension and position for each window
x_0 = monitor.x
y_0 = monitor.y
w = int(monitor.width / 4)  # vl-windows width (a quart of primary monitor width)
h = int(monitor.height / 4)  # vl-windows height (a quart of primary monitor height)
ml = int(w - monitor.width / 16)  # base margin left (w - dw)
mt = int(h - monitor.height / 12)  # base margin top (h - dh)
dimension = str(w) + 'x' + str(h) + '+'

current_state = [
    dict(vl_number=1, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(x_0) + '+' + str(y_0)),
    dict(vl_number=2, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(x_0 + ml) + '+' + str(y_0 + mt)),
    dict(vl_number=3, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(x_0 + 2 * ml) + '+' + str(y_0 + 2 * mt)),
    dict(vl_number=4, vl_instance=initial, action=initial,
         w_h_x_y=dimension + str(x_0 + 3 * ml) + '+' + str(y_0 + 3 * mt))
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
def destroy_window(state, new_action):
    state['window'].destroy()
    state['vl_instance'].stop()

    state.update(
        {'action': new_action, 'vl_instance': '', 'window': ''})


# MAKE THE SPECIFIED WINDOW ON FOCUS
def focus_window(vl_number):
    subprocess.run(['wmctrl', '-a', 'Video Lan ' + str(vl_number)])


class ConsumerThread(threading.Thread):
    def __init__(self, q_msg):
        threading.Thread.__init__(self)
        self.q_msg = q_msg

    def run(self):
        global new_msg

        while True:
            # time.sleep(0.1)
            array_msg = self.q_msg.get(True).split(',')
            if len(array_msg) > 1:
                new_msg.update({
                    'vl': int(array_msg[1]),
                    'action': array_msg[0]
                })
                print(f"consumer thread, consuming: {new_msg} \n")
            else:
                root.destroy()
                os.kill(os.getpid(), signal.SIGINT)


# TODO on 'esc' i can close all the windows and close the connection but remain always a pending lock
class VideoLanThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global lock
        global current_state
        global new_msg
        while True:
            vl = new_msg['vl']
            lock.acquire()

            if vl != 0:  # action != ''
                state = current_state[vl - 1]
                new_action = new_msg['action']
                current_action = state['action']
                current_vl_instance = state['vl_instance']

                # START ACTION
                if new_action == 'start':
                    print(f"{self.name}: {new_action} vl {vl}\n")
                    os.chdir("/home/human/Video")

                    # PLAY
                    if current_vl_instance == '':
                        create_window(vl, root, state, new_action)

                    # REPLAY
                    else:
                        destroy_window(state, new_action)
                        time.sleep(0.1)
                        create_window(vl, root, state, new_action)

                # STOP ACTION
                elif (new_action == 'stop') and (new_action != current_action) and (current_vl_instance != ''):
                    print(f"{self.name}: {new_action} vl {vl}\n")
                    destroy_window(state, new_action)

                # FOCUS ACTION
                elif new_action == 'focus' and \
                        current_action == 'start':
                    print(f"{self.name}: {new_action} vl {vl}\n")
                    focus_window(vl)

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
