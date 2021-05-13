import sys
from tkinter.constants import BOTTOM, LEFT, NSEW, RIGHT, TOP
sys.path.insert(0, '../../utility')
import tkinter as tk
from mysocket import MySocket

class Server:
    def __init__(self):
        super().__init__()
        # Initialize socket
        self.IP = ("127.0.0.1", 54321)
        # Initialize GUI
        self._root = tk.Tk()
        self._root.geometry("1000x800")
        self._root.title("Library Server")
        self._root.lbl_title = tk.Label(self._root, text = "ONLINE LIBRARY SERVER", width = 25,
                                            font = ("Consolas 30 bold"), fg = "#ff0000")
        self._root.lbl_address = tk.Label(self._root, text = "Address: " + str(self.IP[0]), width = 25,
                                            font = ("Consolas 25 bold"))
        self._root.lbl_logs = tk.Label(self._root, text = "Message:", width = 25,
                                            font = ("Consolas 15 bold")
        )
        self._root.btn_disconnect = tk.Button(self._root, text = "DISCONNECT", width = 12, 
                                            font = "Consolas 20 bold")
        
        self._root.logs = tk.Text(self._root, width = 115, height = 40)
        self._root.lbl_title.pack()
        self._root.lbl_address.pack(pady = (5, 25))
        self._root.lbl_logs.pack(side = TOP, anchor = "w")
        self._root.btn_disconnect.pack(side = BOTTOM, anchor = "e", pady = 30, padx = 50)
        self._root.logs.pack(side = BOTTOM)
        
    def runApplication(self):
        self._root.mainloop()
        
x = Server()
x.runApplication()