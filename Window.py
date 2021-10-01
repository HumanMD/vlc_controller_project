from tkinter import *


class Window(Toplevel):
    nid = 0
    vl_instance = ""

    def __init__(self, master, nid, title, vl_instance):
        Toplevel.__init__(self, master)
        self.nid = nid
        self.title(title)  # since toplevel widgets define a method called title you can't store it as an attribute
        self.vl_instance = vl_instance
        self.display_gui()  # maybe just leave that code part of the __init__?

    def display_gui(self):
        '''Tkinter to create a gui window with parameters '''
        # no window, just self
        self.geometry("800x600")
        xid = self.winfo_id()
        self.vl_instance.set_xwindow(xid)
        # self.configure(background="#BAD0EF")
        # pass self as the parent to all the child widgets instead of window
        title = Entry(self, relief=FLAT, bg="#BAD0EF", bd=0)

        # title.pack(side=TOP)
        # scrollBar = Scrollbar(self, takefocus=0, width=20)
        # textArea = Text(self, height=4, width=1000, bg="#BAD0EF", font=("Times", "14"))
        # scrollBar.pack(side=RIGHT, fill=Y)
        # textArea.pack(side=LEFT, fill=Y)
        # scrollBar.config(command=textArea.yview)
        # textArea.config(yscrollcommand=scrollBar.set)
        # textArea.insert(END, self.message)
        # self.mainloop() #leave this to the root window

        def run(self):
            self.display_gui()
