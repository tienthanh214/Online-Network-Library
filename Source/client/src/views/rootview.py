import mysocket as msk
import tkinter as tk
from tkinter import font as tkfont
from socket import AF_INET, SOCK_STREAM

from login import Login
from signup import Signup
from connect import Connect
from search import Search
from book import Book
import dialog as box

import sys
sys.path.insert(0, '../../../utility')


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
        # !!!!!!! MySocket is imcomplete
        self._socket = msk.MySocket(AF_INET, SOCK_STREAM)

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
        try:
            self._socket.send(bytes(page_name.upper()), "utf8")
        except:
            pass
        finally:
            self.frame = self.frames[page_name]
            self.frame.tkraise()

    def connect(self):
        '''Connect to the library server'''
        ip, port = frame.get_info()

        if ip.strip(' ') == "":
            box.messagebox("Connect", "Please enter an IP address", "warn")
            return
        if port.strip(' ') == "":
            box.messagebox("Connect", "Please enter a port number", "warn")
            return

        try:
            self._socket.connect((ip, int(port)))
            box.messagebox("Connect", "Connected to the library", "info")
        except:
            box.messagebox("Connect", "Unable to connect", "error")

    def login(self):
        '''Send name and password to the server for authentication'''
        usr, pas = self.frame.get_info()

        if usr.strip(' ') == "":
            box.messagebox("Connect", "Please enter your username", "warn")
            return
        if pas.strip(' ') == "":
            box.messagebox("Connect", "Please enter your password", "warn")
            return

        try:
            self._socket.send(bytes(','.join(["login", usr, pas]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "success":
                box.messagebox("Log in", "Welcome " + usr, "info")
                self.username = usr
                self.show_frame("Search")
            else:
                box.messagebox("Log in", response, "warn")
        except:
            box.messagebox("Log in", "Unable to send request", "error")

    def signup(self):
        '''Create new account if it is not yet existed'''
        usr, pas, num = self.frame.get_info()

        if usr.strip(' ') == "":
            box.messagebox("Sign up", "Please enter your username", "warn")
            return
        if pas.strip(' ') == "":
            box.messagebox("Sign up", "Please enter your password", "warn")
            return
        if num.strip(' ') == "":
            box.messagebox("Sign up", "Please enter your phone number", "warn")
            return

        try:
            self._socket.send(
                bytes(','.join(["signup", usr, pas, num]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "success":
                box.messagebox(
                    "Log in", "Account created, please go\nback to log in page", "info")
            else:
                box.messagebox("Log in", response, "warn")
        except:
            box.messagebox("Connect", "Unable to send request", "error")
        pass

    def search(self):
        '''Send the search query to the server'''
        query = self.frame.get_query()

        try:
            self._socket.send(bytes(query), "utf8")
            response = self._socket.receive().decode("utf8")
            # do something
            self.frame.show_result(to_matrix(response))
        except:
            box.messagebox("Connect", "Unable to send request", "error")
        pass

    def book(self):
        '''Display book title and content in a seperate window'''
        bookid = self.frame.get_bookid()

        try:
            self._socket.send(bytes(','.join(["book", bookid]), "utf8"))
            response = self._socket.receive().decode("utf8")
            Book(tk.Tk(), *response.split('\n', 1))
            # do something
        except:
            box.messagebox("View book", "Unable to retrieve book", "error")

    def logout(self):
        '''Erase info and return to login screen'''
        self._socket.send(bytes("LOGOUT"), "utf8")
        self.username = "<N/A>"
        self.show_frame("Login")


if __name__ == "__main__":
    app = RootView()
    app.run()
