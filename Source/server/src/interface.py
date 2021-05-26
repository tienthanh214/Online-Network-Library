import time
import pickle
import tkinter as tk
from threading import Thread
import tkinter.scrolledtext as tkst
from src.database import DataBase
from src.manager import Manager
from src.mysocket import *

MAXIMUM_CONNECTION = 10

class Server:
    def __init__(self):
        super().__init__()
        # Initialize socket
        self.IP = (sk.gethostbyname(sk.gethostname()), 54321)
        self.server = MySocket(sk.AF_INET, sk.SOCK_STREAM)
        self.server.bind(self.IP)
        self.server.listen(MAXIMUM_CONNECTION) # maximum 5 client
        self.clients_list = {}
        # Initialize GUI
        self._root = tk.Tk()
        self._root.geometry("1000x800")
        self._root.configure(bg = '#7ed6df')
        self._root.title("Online Library Server")
        self._root.button_frame = tk.Frame(self._root, bg = '#7ed6df')
        ## Create widgets
        self._root.lbl_title = tk.Label(self._root, text = "ONLINE LIBRARY SERVER", width = 25,
                                            font = "Consolas 30 bold", bg = '#f9cdad', fg = "#ec2049")
        self._root.lbl_address = tk.Label(self._root, text = "Address: " + str(self.IP[0]), width = 25,
                                            font = "Consolas 25 bold", bg = '#fc9d9a', fg = '#aa2e00')
        self._root.lbl_logs = tk.Label(self._root, text = "Message:", width = 15,
                                            font = "Consolas 15 bold", bg = '#97c1a9', fg = '#ffffff')
        self._root.btn_disconnect = tk.Button(self._root.button_frame, text = "DISCONNECT", width = 12, 
                                            activebackground = "#ff8c94", bg = "#355c7d", fg = '#feffff',
                                            font = "Consolas 20 bold", command = self.on_exit_main)
        self._root.btn_manager = tk.Button(self._root.button_frame, text = "MANAGER", width = 12,
                                            activebackground = "#ff8c94", bg = "#355c7d", fg = "#feffff",
                                            disabledforeground = "#f9c859",
                                            font = "Consolas 20 bold", command = self.on_manager)
        self._root.logs = tkst.ScrolledText(self._root, width = 95, height = 25, state = "disable",
                                            font = ("Consolas 14 bold"), wrap = tk.WORD, bg = "#c7ecee", foreground = "#2a363d")
        
        # Setup button function
        self._root.bind("<Destroy>", self.on_exit_main)
        # Draw widgets
        self._root.lbl_title.pack(pady = (20, 0))
        self._root.lbl_address.pack(pady = (0, 10))
        self._root.lbl_logs.pack(side = tk.TOP, anchor = "w", padx = 15)
        self._root.button_frame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = 1, pady = 40)
        self._root.btn_manager.pack(side = tk.LEFT, padx = 40)
        self._root.btn_disconnect.pack(side = tk.RIGHT, padx = 40)
        self._root.logs.pack(side = tk.BOTTOM)
        # Initialize Database
        self.db = DataBase()
        # Running server
        Thread(target = self.accept_connections, daemon = True).start()
        self.update_logs(Server.get_message(msg = "SERVER STARTED"))
        
    def runApplication(self):
        self._root.mainloop()
    
    def on_exit_main(self, event = None):
        for client in self.clients_list:
            client.close()
            self.update_logs(Server.get_message(self.clients_list[client], msg = "QUIT command from Server"))
        del self.clients_list
        self.clients_list = {}

    def on_manager(self, event = None):
        self._root.btn_manager.config(state = 'disable')
        self._root.manager = Manager(self._root, self.db)
        def quit_win():
            self._root.manager.manager.destroy()
            self._root.btn_manager.config(state = 'normal')

        self._root.manager.manager.protocol("WM_DELETE_WINDOW", quit_win)

    @staticmethod
    def get_message(addr = None, user = None, msg = None):
        result = '[' + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()) + ']\t'
        if addr: result += str(addr) + '\t'
        if user: result += "'" + user + "'\t"
        result += msg
        return result

    def update_logs(self, msg):
        if not msg: return
        self._root.logs.configure(state = "normal")
        self._root.logs.insert(tk.END, msg + '\n')
        self._root.logs.see(tk.END)
        self._root.logs.configure(state = "disable")

    def accept_connections(self):
        """ Multithreading handling for incomming clients"""
        while True:
            client, addr = self.server.accept()
            if len(self.clients_list) >= MAXIMUM_CONNECTION:
                client.send(bytes("OVERFLOW", "utf8"))
                client.close()
                continue
            client.send(bytes("OK", "utf8"))
            self.clients_list[client] = addr
            self.update_logs(Server.get_message(addr, msg = "CONNECTED TO SERVER"))
            Thread(target = self.handle_client, args = (client, addr, )).start()


    def handle_client(self, client, addr):
        """ Handles a single client connection """
        USER = None
        while True:
            try:
                msg = client.recv(1024).decode("utf8")
            except OSError: # client
                break
            if (msg == "QUIT"):
                self.update_logs(Server.get_message(addr, msg = "QUIT"))
                client.shutdown(sk.SHUT_RDWR)
                client.close()
                del self.clients_list[client]
                return
            else:
                if not USER: # chua login
                    cmd = msg.split('\t')
                    if cmd[0] == 'LOGIN':
                        ''' ---------- Handle login ----------'''
                        respone = self.db.account_sign_in(cmd[1], cmd[2])
                        if respone == "SUCCESS":
                            USER = cmd[1]
                        client.send(bytes(respone, "utf8"))
                        self.update_logs(Server.get_message(addr, 
                                        msg = ("'" + cmd[1] + "' ") + "HAS LOGIN " + respone))
                        ''' ---------------------------------------------------------------- '''
                    elif cmd[0] == 'SIGNUP':
                        ''' ---------- Handle signup ----------'''
                        respone = self.db.account_sign_up(cmd[1], cmd[2])
                        client.send(bytes(respone, "utf8"))
                        self.update_logs(Server.get_message(addr,
                                        msg = "'" + cmd[1] + "' HAS SIGN UP " + respone))
                        ''' ---------------------------------------------------------------- '''
                else: # loged-in
                    cmd = msg.split('\t', 1)
                    if cmd[0] == 'SEARCH':
                        result = pickle.dumps(self.db.book_query(cmd[1]))
                        client.send(result)
                        self.update_logs(Server.get_message(addr, USER, msg))
                        self.update_logs(Server.get_message("SERVER", msg = "send search result to " + str(addr)))
                        
                    elif cmd[0] == 'BOOK':
                        try:
                            client.send(bytes(self.db.get_book(cmd[1]), "utf8"))
                            self.update_logs(Server.get_message(addr, USER, "READ BOOK with ID = " + cmd[1]))
                            self.update_logs(Server.get_message("SERVER", msg = "send book to " + str(addr)))
                        except FileNotFoundError:
                            client.send(bytes("Book not available", "utf8"))
                            self.update_logs(Server.get_message(addr, USER, "READ BOOK with ID = " + cmd[1] + " but book not found"))

                    elif cmd[0] == 'LOGOUT':
                        self.update_logs(Server.get_message(addr, USER, "has LOGGED OUT"))
                        USER = None
                    
                    elif cmd[0] == 'DOWNLOAD':
                        self.update_logs(Server.get_message(addr, USER, "DOWNLOAD BOOK with ID = " + cmd[1]))
                pass
            pass
        pass
    pass