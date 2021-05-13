import tkinter as tk
from tkinter import font as tkfont

from login import Login
from signup import Signup
from connect import Connect
from search import Search
from book import Book
import dialog as box

import sys
sys.path.insert(0, '../../../utility')
import mysocket as msk

class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # predefined fonts for UI consistency
        self.title_font = tkfont.Font(
            family='Helvetica', size=12, weight="bold", slant="roman")
        self.label_font = tkfont.Font(
            family='Helvetica', size=10, weight="bold", slant="roman")
        self.user_font = tkfont.Font(
            family='Helvetica', size=14, weight="normal", slant="italic")

        # socket to send and receive data
        self._socket = msk.MySocket()

        # use tkraise to show frame above the other
        self.container = tk.Frame(self)
        self.geometry("768x560+50+50")
        self.title("Online Library")
        self.resizable(False, False)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.grid()

        self.username = "<N/A>"

        self.frames = {}
        for F in (Login, Signup, Connect, Search):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.show_frame("Connect")
        self.mainloop()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def connect(self):
        frame = self.frames["Connect"]
        [ip, port] = frame.get_info()
        if ip.strip(' ') == "":
            box.messagebox("Connect", "Enter your username", "warn")
        if port.strip(' ') == "":
            box.messagebox("Connect", "Enter your password", "warn")
        self._socket.connect((ip, int(port)))
        pass

    def login(self):
        frame = self.frames["Login"]
        pass

    def signup(self):
        frame = self.frames["Signup"]
        pass

    def search(self):
        frame = self.frames["Search"]
        pass

    def book(self):
        pass


if __name__ == "__main__":
    app = RootView()
    app.run()
