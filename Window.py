from tkinter import *


class Window(Toplevel):
    nid = 0
    vl_instance = ""

    def __init__(self, master, nid, title, vl_instance, w_h_x_y):
        Toplevel.__init__(self, master)
        self.w_h_x_y = w_h_x_y
        self.nid = nid
        self.title(title)  # since toplevel widgets define a method called title you can't store it as an attribute
        self.vl_instance = vl_instance
        self.display_gui()

    def display_gui(self):
        """Tkinter to create a gui window with parameters """
        # no window, just self
        xid = self.winfo_id()
        self.vl_instance.set_xwindow(xid)
        self.geometry(self.w_h_x_y)
        # pass self as the parent to all the child widgets instead of window
        title = Entry(self, relief=FLAT, bg="#000000", bd=0)

    def run(self):
        self.display_gui()