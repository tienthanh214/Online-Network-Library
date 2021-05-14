import sys
# sys.path.insert(0, '../../utility')
from src.mysocket import *
import time
import pickle
import tkinter as tk
from threading import Thread
from src.database import DataBase

class Server:
    def __init__(self):
        super().__init__()
        # Initialize socket
        self.IP = (sk.gethostbyname(sk.gethostname()), 54321)
        self.server = MySocket(sk.AF_INET, sk.SOCK_STREAM)
        self.server.bind(self.IP)
        self.server.listen(5) # maximum 5 client
        self.clients_list = {}
        Thread(target = self.accept_connections, daemon = True).start()
        # Initialize GUI
        self._root = tk.Tk()
        self._root.geometry("1000x800")
        self._root.title("Online Library Server")
        self._root.lbl_title = tk.Label(self._root, text = "ONLINE LIBRARY SERVER", width = 25,
                                            font = "Consolas 30 bold", fg = "#ff0000")
        self._root.lbl_address = tk.Label(self._root, text = "Address: " + str(self.IP[0]), width = 25,
                                            font = "Consolas 25 bold")
        self._root.lbl_logs = tk.Label(self._root, text = "Message:", width = 25,
                                            font = "Consolas 15 bold")
        self._root.btn_disconnect = tk.Button(self._root, text = "DISCONNECT", width = 12, 
                                            font = "Consolas 20 bold", command = self.on_exit)
        self._root.logs = tk.Text(self._root, width = 95, height = 40, state = "disable",
                                            font = "Consolas 14")
        # Draw widget
        self._root.lbl_title.pack()
        self._root.lbl_address.pack(pady = (5, 25))
        self._root.lbl_logs.pack(side = tk.TOP, anchor = "w")
        self._root.btn_disconnect.pack(side = tk.BOTTOM, anchor = "e", pady = 30, padx = 50)
        self._root.logs.pack(side = tk.BOTTOM)
        # Setup button function
        self._root.bind("<Destroy>", self.on_exit)
        # Initialize Database
        self.db = DataBase()
        
    def runApplication(self):
        self._root.mainloop()
    
    def on_exit(self, event = None):
        for client in self.clients_list:
            client.close()
            self.update_logs(Server.get_message(self.clients_list[client], "QUIT command from Server"))

        del self.clients_list
        self.clients_list = {}

    @staticmethod
    def get_message(user, msg):
        result = '[' + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()) + ']\t'
        result += '<' + str(user) + '>\t'
        result += msg
        return result

    def update_logs(self, msg):
        if not msg: return
        self._root.logs.configure(state = "normal")
        self._root.logs.insert(tk.END, msg + '\n')
        self._root.logs.configure(state = "disable")
        

    def accept_connections(self):
        """ Multithreading handling for incomming clients"""
        while True:
            client, addr = self.server.accept()
            self.clients_list[client] = addr
            self.update_logs(Server.get_message(addr, "CONNECTED TO SERVER"))
            Thread(target = self.handle_client, args = (client, )).start()


    def handle_client(self, client):
        """ Handles a single client connection """
        USER = None
        while True:
            try:
                msg = client.recv(1024).decode("utf8")
            except OSError: # client
                break
            print(self.clients_list[client], msg)
            if (msg == "QUIT"):
                self.update_logs(Server.get_message(self.clients_list[client], "QUIT"))
                client.shutdown(sk.SHUT_RDWR)
                client.close()
                del self.clients_list[client]
                return
            else:
                if not USER: # chua login
                    cmd = msg.split('\t')
                    if cmd[0] == 'LOGIN':
                        respone = self.db.account_sign_in(cmd[1], cmd[2])
                        if respone == "SUCCESS":
                            USER = cmd[1]
                        client.send(bytes(respone, "utf8"))

                    elif cmd[0] == 'SIGNUP':
                        respone = self.db.account_sign_up(cmd[1], cmd[2])
                        client.send(bytes(respone, "utf8"))

                else: # loged-in
                    cmd = msg.split('\t', 1)
                    if cmd[0] == 'SEARCH':
                        result = pickle.dumps(self.db.book_query(cmd[1]))
                        client.send(result)
                    elif cmd[0] == 'BOOK':
                        client.send(bytes(self.db.get_book(cmd[1]), "utf8"))
                    elif cmd[0] == 'LOGOUT':
                        USER = None
                pass
            pass
        pass