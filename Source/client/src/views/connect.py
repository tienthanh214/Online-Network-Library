import tkinter as tk
import src.views.textstyles as style


class Connect(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        self.spacer = tk.Label(self, height=4, width=30, anchor=tk.E)
        self.spacer.grid(row=0, column=0)

        self.lbl_ip = tk.Label(
            self, height=1, text="IP address:", width=40, justify="left", font=style.label_font, anchor=tk.W)
        self.lbl_ip.grid(row=1, column=1, sticky=tk.E+tk.W,
                         padx=10, pady=0, columnspan=1)
        self.txt_ip = tk.Entry(self, width=60, bg="#FFFFFF")
        self.txt_ip.grid(row=2, column=1, sticky=tk.E,
                         padx=10, pady=10, columnspan=1)

        self.lbl_port = tk.Label(
            self, height=1, text="Port number:", width=40, justify="left", font=style.label_font, anchor=tk.W)
        self.lbl_port.grid(row=3, column=1, sticky=tk.E+tk.W,
                           padx=10, pady=0, columnspan=1)
        self.txt_port = tk.Entry(self, width=60, bg="#FFFFFF")
        self.txt_port.grid(row=4, column=1, sticky=tk.E,
                           padx=10, pady=10, columnspan=1)

        self.btn_connect = tk.Button(
            self, text="Connect", width=10, height=2)
        self.btn_connect.grid(row=5, column=1, sticky=tk.S +
                              tk.N, padx=10, pady=10, columnspan=1)

    def get_info(self):
        ip = self.txt_ip.get()
        port = self.txt_port.get()
        return ip, port
