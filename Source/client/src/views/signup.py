import tkinter as tk


class Signup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.lbl_username = tk.Label(
            self, height=1, text="Username:", width=20, justify="left")
        self.lbl_username.grid(row=0, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_username = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_username.grid(row=0, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)
        
        self.lbl_password = tk.Label(
            self, height=1, text="Password:", width=20, justify="left")
        self.lbl_password.grid(row=1, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_password = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_password.grid(row=1, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)
        
        self.btn_signup = tk.Button(
            self, text="Sign up", width=10, height=2)
        self.btn_signup.grid(row=2, column=2, sticky=tk.N,
                             padx=10, pady=10, columnspan=1)

    def get_info(self):
        usr = self.txt_username.get("1.0", tk.END)
        pas = self.txt_password.get("1.0", tk.END)
        return ','.join([usr, pas])
