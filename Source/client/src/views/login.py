import tkinter as tk
import src.views.textstyles as style


class Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        self.lbl_username = tk.Label(
            self, height=1, text="Username:", width=20, justify="left", font=style.label_font, anchor=tk.E)
        self.lbl_username.grid(row=0, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_username = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_username.grid(row=0, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)

        self.lbl_password = tk.Label(
            self, height=1, text="Password:", width=20, justify="left", font=style.label_font, anchor=tk.E)
        self.lbl_password.grid(row=1, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_password = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_password.grid(row=1, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)

        self.btn_login = tk.Button(
            self, text="Log in", width=10, height=2)
        self.btn_login.grid(row=2, column=1, sticky=tk.E,
                            padx=10, pady=10, columnspan=1)

        self.btn_signup = tk.Button(
            self, text="Sign up", width=10, height=2)
        self.btn_signup.grid(row=2, column=2, sticky=tk.W,
                             padx=10, pady=10, columnspan=1)

    def get_info(self):
        usr = self.txt_username.get("1.0", tk.END).strip('\n')
        pas = self.txt_password.get("1.0", tk.END).strip('\n')
        return usr, pas
