import sys
sys.path.insert(0, '../../utility')
import tkinter as tk
from mysocket import MySocket

class Server:
    def __init__(self):
        super().__init__()
        # Initialize GUI
        self._root = tk.Tk()
        self._root.geometry("1000x900")
        self._root.title("Library Server")
        self._root.lbl_title = tk.Label(self._root, text = "ONLINE LIBRARY SERVER", width = 25,
                                            font = ("Consolas 30 bold"), fg = "#ff0000")
        self._root.logs = tk.Text(self._root, width = 115, height = 40)
        # self._root.logs.grid(row = 1, column = 0, sticky = tk.N, padx = 10, pady = 10, columnspan = 3)
        # self._root.logs.place(relx = 0.5, rely = 0.65, anchor = tk.CENTER)
        # self._root.lbl_title.grid(row = 0, column = 0, sticky = tk.N)
        # self._root.logs.grid(column = 0, row = 0, sticky = "EW")
        self._root.lbl_title.grid(column = 0, row = 0)
        self._root.lbl_title.grid(row = 1, column = 0)

        #self._root.logs.place(x = 50, y = 100)
        
    def runApplication(self):
        self._root.mainloop()
        
x = Server()
x.runApplication()