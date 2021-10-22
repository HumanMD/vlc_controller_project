import time
from tkinter import *


class Window(Toplevel):
    vl_instance = ""

    def __init__(self, master, title, vl_instance, w_h_x_y):
        Toplevel.__init__(self, master)
        self.w_h_x_y = w_h_x_y
        self.title(title)  # since toplevel widgets define a method called title you can't store it as an attribute
        self.vl_instance = vl_instance
        self.display_gui()

    def display_gui(self):
        """Tkinter to create a gui window """
        xid = self.winfo_id()  # get the x window id
        self.attributes('-alpha', 0)  # the window has initially opacity 0
        self.vl_instance.set_xwindow(xid)  # define video to display inside the x window with id xid
        self.geometry(self.w_h_x_y)  # define the window dimension and position
        self.update_idletasks()  # update the pending task and wait
        time.sleep(0.5)
        self.after_idle(lambda: self.attributes('-alpha', 1))  # make the window visible when updated

    def run(self):
        self.display_gui()
