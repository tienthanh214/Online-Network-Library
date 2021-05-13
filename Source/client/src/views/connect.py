import tkinter as tk


class Connect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.lbl_ip = tk.Label(
            self, height=1, text="IP address:", width=20, justify="left", font=self.controller.label_font, anchor=tk.E)
        self.lbl_ip.grid(row=0, column=0, sticky=tk.W +
                         tk.S+tk.E+tk.N,
                         padx=10, pady=0, columnspan=1)
        self.txt_ip = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_ip.grid(row=0, column=1, sticky=tk.W +
                         tk.S+tk.E+tk.N,
                         padx=10, pady=10, columnspan=3)
        
        self.lbl_port = tk.Label(
            self, height=1, text="Port number:", width=20, justify="left", font=self.controller.label_font, anchor=tk.E)
        self.lbl_port.grid(row=1, column=0, sticky=tk.W +
                           tk.S+tk.E+tk.N,
                           padx=10, pady=0, columnspan=1)
        self.txt_port = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_port.grid(row=1, column=1, sticky=tk.W +
                           tk.S+tk.E+tk.N,
                           padx=10, pady=10, columnspan=3)
        
        self.btn_connect = tk.Button(
            self, text="Connect", width=10, height=2)
        self.btn_connect.grid(row=2, column=2, sticky=tk.W +
                              tk.S+tk.E+tk.N,
                              padx=10, pady=10, columnspan=1)

    def get_info(self):
        ip = self.txt_ip.get("1.0", tk.END)
        port = self.txt_port.get("1.0", tk.END)
        return ','.join([ip, port])
