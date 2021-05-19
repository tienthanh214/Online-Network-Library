import tkinter as tk
import src.views.textstyles as style


class Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        self.spacer = tk.Label(self, height=5, width=30, anchor=tk.E)
        self.spacer.grid(row=0, column=0)

        self.lbl_username = tk.Label(
            self, height=1, text="Username:", width=40, justify="left", font=style.label_font, anchor=tk.W)
        self.lbl_username.grid(row=1, column=1, sticky=tk.E+tk.W,
                               padx=10, pady=0, columnspan=2)
        self.txt_username = tk.Entry(self, width=60, bg="#FFFFFF")
        self.txt_username.grid(row=2, column=1, sticky=tk.E,
                               padx=10, pady=10, columnspan=2)

        self.lbl_password = tk.Label(
            self, height=1, text="Password:", width=40, justify="left", font=style.label_font, anchor=tk.W)
        self.lbl_password.grid(row=3, column=1, sticky=tk.E+tk.W,
                               padx=10, pady=0, columnspan=2)
        self.txt_password = tk.Entry(self, show="*", width=60, bg="#FFFFFF")
        self.txt_password.grid(row=4, column=1, sticky=tk.E,
                               padx=10, pady=10, columnspan=2)

        self.btn_login = tk.Button(
            self, text="Log in", width=10, height=2)
        self.btn_login.grid(row=5, column=1, sticky=tk.E,
                            padx=10, pady=10, columnspan=1)

        self.btn_newacc = tk.Button(
            self, text="New account", width=10, height=2)
        self.btn_newacc.grid(row=5, column=2, sticky=tk.W,
                             padx=10, pady=10, columnspan=1)

    def get_info(self):
        usr = self.txt_username.get()
        pas = self.txt_password.get()
        return usr, pas

    def clear_all(self):
        self.txt_username.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
