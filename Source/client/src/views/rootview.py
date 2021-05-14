import tkinter as tk

from socket import AF_INET, SOCK_STREAM
from login import Login
from signup import Signup
from connect import Connect
from search import Search
from book import Book
from mysocket import MySocket
from dialog import messagebox


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._socket = MySocket(AF_INET, SOCK_STREAM)
        self.username = "<N/A>"

        self.container = tk.Frame(self)
        self.geometry("768x560+50+50")
        self.title("Online Library")
        self.resizable(False, False)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}
        self.create_frames()
        self.bind_action()

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.show_frame("Connect")
        self.mainloop()

    def create_frames(self):
        '''Init instances of frames and store in a map'''
        for frame in (Login, Signup, Connect, Search):
            page_name = frame.__name__
            instance = frame(parent=self.container)
            instance.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = instance

    def bind_action(self):
        '''Bind button with actions'''
        self.bind("<Destroy>", lambda e:self.quit_prog())

        self.frames["Connect"].btn_connect["command"] = self.connect

        self.frames["Login"].btn_login["command"] = self.login
        self.frames["Login"].btn_signup["command"] = lambda: self.show_frame(
            "Signup")

        self.frames["Signup"].btn_signup["command"] = lambda: self.signup
        self.frames["Signup"].btn_back["command"] = lambda: self.show_frame(
            "Login")

        self.frames["Search"].btn_search["command"] = self.search
        self.frames["Search"].btn_logout["command"] = self.logout
        self.frames["Search"].tbl_result.bind(
            "<Double-1>", lambda e: self.book())

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        try:
            if not page_name == "Connect":
                self._socket.send(bytes(page_name.upper()), "utf8")
            self.frame = self.frames[page_name]
            self.frame.tkraise()
        except:
            messagebox("Lost connection", "Cannot contact to the server", "error")

    def connect(self):
        '''Connect to the library server'''
        ip, port = self.frame.get_info()

        if ip.strip(' ') == "":
            messagebox("Invalid input", "Please enter an IP address", "warn")
            return
        if port.strip(' ') == "":
            messagebox("Invalid input", "Please enter a port number", "warn")
            return

        try:
            self._socket.connect((ip, int(port)))
            messagebox("Accepted", "Connected to the library", "info")
        except:
            messagebox("Failed", "Unable to connect, please try again", "error")

    def login(self):
        '''Send name and password to the server for authentication'''
        usr, pas = self.frame.get_info()

        if usr.strip(' ') == "":
            messagebox("Invalid input", "Please enter your username", "warn")
            return
        if pas.strip(' ') == "":
            messagebox("Invalid input", "Please enter your password", "warn")
            return

        try:
            self._socket.send(bytes('\t'.join([usr, pas]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "SUCCESS":
                messagebox("Log in successful", "Welcome, " + usr, "info")
                self.username = usr
                self.show_frame("Search")
            else:
                errmsg = response.split(' ', 1)[1]
                messagebox("Log in failed", errmsg, "warn")
        except:
            messagebox("Log in", "Unable to send request", "error")

    def signup(self):
        '''Create new account if it is not yet existed'''
        usr, pas, num = self.frame.get_info()

        if usr.strip(' ') == "":
            messagebox("Invalid input", "Please enter your username", "warn")
            return
        if pas.strip(' ') == "":
            messagebox("Invalid input", "Please enter your password", "warn")
            return
        if num.strip(' ') == "":
            messagebox("Invalid input",
                       "Please enter your phone number", "warn")
            return

        try:
            self._socket.send(bytes('\t'.join([usr, pas]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "SUCCESS":
                messagebox(
                    "Sign up successful", "Account created, please go\nback to log in page", "info")
            else:
                errmsg = response.split(' ', 1)[1]
                messagebox("Sign up failed", errmsg, "warn")
        except:
            messagebox("Connect", "Unable to send request", "error")
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
            messagebox("Connect", "Unable to send request", "error")
        pass

    def book(self):
        '''Display book title and content in a seperate window'''
        bookid = self.frame.get_bookid()

        try:
            self._socket.send(bytes(','.join(["get", bookid]), "utf8"))
            response = self._socket.receive().decode("utf8")
            Book(tk.Tk(), *response.split('\t', 1))
            # do something
        except:
            messagebox("View book", "Unable to retrieve book", "error")

    def logout(self):
        '''Erase info and return to login screen'''
        self._socket.send(bytes("LOGOUT"), "utf8")
        self.frames["Search"].clear_result()
        self.username = "<N/A>"
        self.show_frame("Login")

    def quit_prog(self):
        '''Close the window and shut down program'''
        self._socket.send(bytes("QUIT"), "utf8")
        self._socket.close()

    def to_matrix(self):
        pass