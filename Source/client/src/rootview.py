import tkinter as tk
import pickle
import src.views.textstyles as style

from socket import AF_INET, SOCK_STREAM
from src.views.login import Login
from src.views.signup import Signup
from src.views.connect import Connect
from src.views.search import Search
from src.views.book import Book
from src.views.dialog import messagebox
from src.mysocket import MySocket


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._socket = MySocket(AF_INET, SOCK_STREAM)
        self.username = "<N/A>"

        self.geometry("800x640+50+50")
        self.title("Online Library")
        self.resizable(False, False)
        self.grid()

        # Header
        self.head = tk.Frame(self, bg="#6495ED")
        self.head.pack(side="top", fill="both", expand=True)
        self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(0, weight=1)

        # Body
        self.body = tk.Frame(self)
        self.body.pack(side="top", fill="both", expand=True)
        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        # Create widgets
        self.frame = None
        self.frames = {}
        self.create_header()
        self.create_frames()
        self.bind_action()

    def run(self):
        '''Run the UI loop and show the connect page'''
        self.show_frame("Connect")
        self.mainloop()

    def create_header(self):
        '''Init header element'''
        self.lbl_app = tk.Label(
            self.head, text='HCMUS Online Library', height=1, font=style.logo_font, bg="white")
        self.lbl_app.grid(row=0, column=0, sticky=tk.W, padx=30,
                          ipadx=10, ipady=10, columnspan=2, rowspan=2)

        self.lbl_user = tk.Label(
            self.head, text=self.username, height=1, bg="#6495ED", fg="white", font=style.user_font)
        self.lbl_user.grid(row=0, column=2, sticky=tk.E,
                           padx=10, pady=0, columnspan=1)

        self.btn_logout = tk.Button(
            self.head, text="Log out", state=tk.DISABLED, width=6, height=1)
        self.btn_logout.grid(row=0, column=3, sticky=tk.E,
                             padx=10, pady=0)

    def create_frames(self):
        '''Init instances of frames and store in a map'''
        for frame in (Login, Signup, Connect, Search):
            page_name = frame.__name__
            instance = frame(parent=self.body)
            instance.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = instance

    def bind_action(self):
        '''Bind button with actions'''
        self.bind("<Destroy>", self.quit_prog)
        self.btn_logout["command"] = self.logout

        self.frames["Connect"].btn_connect["command"] = self.connect

        self.frames["Login"].btn_login["command"] = self.login
        self.frames["Login"].btn_signup["command"] = lambda: self.show_frame(
            "Signup")

        self.frames["Signup"].btn_signup["command"] = lambda: self.signup
        self.frames["Signup"].btn_back["command"] = lambda: self.show_frame(
            "Login")

        self.frames["Search"].btn_search["command"] = self.search
        self.frames["Search"].tbl_result.bind(
            "<Double-1>", lambda e: self.book())

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.frame = self.frames[page_name]
        self.frame.tkraise()

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
            self.show_frame("Login")
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
            self._socket.sendall(bytes('\t'.join(["LOGIN", usr, pas]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "SUCCESS":
                messagebox("Log in successful", "Welcome, " + usr, "info")
                self.username = usr
                self.btn_logout['state'] = tk.NORMAL
                self.show_frame("Search")
            else:
                errmsg = response.split(' ', 1)[1]
                messagebox("Log in failed", errmsg, "warn")
        except:
            messagebox("Log in", "Unable to send request", "error")

    def signup(self):
        '''Create new account if it is not yet existed'''
        usr, pas = self.frame.get_info()

        if usr.strip(' ') == "":
            messagebox("Invalid input", "Please enter your username", "warn")
            return
        if pas.strip(' ') == "":
            messagebox("Invalid input", "Please enter your password", "warn")
            return

        try:
            self._socket.sendall(bytes('\t'.join(["SIGNUP", usr, pas]), "utf8"))
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

        if query.strip(' ') == "":
            messagebox("Invalid input", "Please enter a query", "warn")
            return

        try:
            self._socket.sendall(bytes('\t'.join(["SEARCH", query]), "utf8"))
            response = self._socket.receive()
            # do something
            self.frame.show_result(pickle.load(response))
        except:
            messagebox("Connect", "Unable to send request", "error")
        pass

    def book(self):
        '''Display book title and content in a seperate window'''
        bookid = self.frame.get_bookid()

        try:
            self._socket.sendall(bytes('\t'.join(["BOOK", bookid]), "utf8"))
            response = self._socket.receive().decode("utf8")
            Book(tk.Tk(), "fix this", response)
            # do something
        except:
            messagebox("View book", "Unable to retrieve book", "error")

    def logout(self):
        '''Erase info and return to login screen'''
        try:
            self._socket.sendall(bytes("LOGOUT", "utf8"))
        except:
            print("> not connected")
        finally:
            self.frames["Search"].clear_result()
            self.frames["Search"].clear_query()
            self.username = "<N/A>"
            self.btn_logout['state'] = tk.DISABLED
            self.show_frame("Login")

    def quit_prog(self, event):
        '''Close the window and shut down program'''
        try:
            if str(event.widget) == '.':
                self._socket.sendall(bytes("QUIT", "utf8"))
                self._socket.close()
        except:
            print("> not connected")
