import tkinter as tk
import pickle
import src.views.textstyles as style

from socket import AF_INET, SOCK_STREAM
from src.views.login import Login
from src.views.signup import Signup
from src.views.connect import Connect
from src.views.search import Search
from src.views.book import Book
from src.views.dialog import messagebox, yesno
from src.mysocket import MySocket


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._socket = MySocket(AF_INET, SOCK_STREAM)
        self.username = tk.StringVar()
        self.username.set("Not logged in")

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
            self.head, textvariable=self.username, height=1, bg="#6495ED", fg="white", font=style.user_font)
        self.lbl_user.grid(row=0, column=2, sticky=tk.E,
                           padx=10, pady=0, columnspan=1)

        self.btn_logout = tk.Button(
            self.head, text="Log out", width=6, height=1)
        self.btn_logout.grid(row=0, column=3, sticky=tk.E,
                             padx=10, pady=0)
        self.btn_logout.grid_remove()

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
        self.bind("<Tab>", self.focus_next_widget)
        self.bind("<Return>", lambda e: self.enterkey(e))
        self.btn_logout["command"] = self.logout

        self.frames["Connect"].btn_connect["command"] = self.connect

        self.frames["Login"].btn_login["command"] = self.login
        self.frames["Login"].btn_newacc["command"] = lambda: self.show_frame(
            "Signup")

        self.frames["Signup"].btn_signup["command"] = self.signup
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
        ip = self.frame.get_info()

        if ip.strip(' ') == "":
            messagebox("Invalid input", "Please enter an IP address", "warn")
            return

        try:
            self._socket.connect((ip, 54321))
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
                self.username.set(usr)
                self.btn_logout.grid()
                self.show_frame("Search")
            else:
                errmsg = response.split(' ', 1)[1]
                messagebox("Log in failed", errmsg, "warn")
        except:
            if yesno("Unable to connect", "Do you want to logout reconnect?"):
                self.logout()
                self._socket = MySocket(AF_INET, SOCK_STREAM)
                self.show_frame("Connect")

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
            self._socket.sendall(
                bytes('\t'.join(["SIGNUP", usr, pas]), "utf8"))
            response = self._socket.receive().decode("utf8")

            if response == "SUCCESS":
                messagebox(
                    "Sign up successful", "Account created, please go\nback to log in page", "info")
            else:
                errmsg = response.split(' ', 1)[1]
                messagebox("Sign up failed", errmsg, "warn")
        except:
            if yesno("Unable to connect", "Do you want to logout and reconnect?"):
                self.logout()
                self._socket = MySocket(AF_INET, SOCK_STREAM)
                self.show_frame("Connect")

    def search(self):
        '''Send the search query to the server'''
        query = self.frame.get_query()

        analyze = query.split(maxsplit=1)
        try:
            if len(analyze) != 2:
                raise
            if not analyze[0] == "F_ID" and not (analyze[1][0] == analyze[1][len(analyze[1]) - 1] and (analyze[1][0] == '"' or analyze[1][0] == '"')):
                raise
        except:
            messagebox("Invalid input", "Please enter a correct query", "warn")
            return

        query = ' '.join(analyze)

        try:
            self._socket.sendall(bytes('\t'.join(["SEARCH", query]), "utf8"))
            response = self._socket.receive()
            self.frame.show_result(pickle.loads(response))
        except:
            if yesno("Unable to connect", "Do you want to logout and reconnect?"):
                self.logout()
                self._socket = MySocket(AF_INET, SOCK_STREAM)
                self.show_frame("Connect")

    def book(self):
        '''Display book title and content in a seperate window'''
        book = self.frame.get_bookid()
        if not book:
            return
        try:
            self._socket.sendall(bytes('\t'.join(["BOOK", book[0]]), "utf8"))
            response = self._socket.receive().decode("utf8")
            Book(tk.Toplevel(self), book[1], response)
            # do something
        except:
            if yesno("Unable to connect", "Do you want to logout and reconnect?"):
                self.logout()
                self._socket = MySocket(AF_INET, SOCK_STREAM)
                self.show_frame("Connect")

    def logout(self):
        '''Erase info and return to login screen'''
        try:
            self._socket.sendall(bytes("LOGOUT", "utf8"))
        except:
            print("> not connected")
        finally:
            self.username.set("Not logged in")
            self.btn_logout.grid_remove()
            self.frames["Connect"].clear_all()
            self.frames["Login"].clear_all()
            self.frames["Signup"].clear_all()
            self.frames["Search"].clear_result()
            self.frames["Search"].clear_query()
            self.show_frame("Login")

    def quit_prog(self, event):
        '''Close the window and shut down program'''
        try:
            if str(event.widget) == '.':
                self._socket.sendall(bytes("QUIT", "utf8"))
                self._socket.close()
        except:
            print("> not connected")

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def enterkey(self, event):
        if event.widget.master._name == "!connect":
            self.connect()
        elif event.widget.master._name == "!login":
            self.login()
        elif event.widget.master._name == "!signup":
            self.signup()
        elif event.widget.master._name == "!search":
            self.search()
