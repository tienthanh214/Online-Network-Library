import tkinter as tk


class Signup(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        import textstyles as style

        self.lbl_phone = tk.Label(
            self, height=1, text="Phone Number:", width=20, justify="left", font=style.label_font, anchor=tk.E)
        self.lbl_phone.grid(row=0, column=0, sticky=tk.E,
                            padx=10, pady=0, columnspan=1)
        self.txt_phone = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_phone.grid(row=0, column=1, sticky=tk.W,
                            padx=10, pady=10, columnspan=3)

        self.lbl_username = tk.Label(
            self, height=1, text="Username:", width=20, justify="left", font=style.label_font, anchor=tk.E)
        self.lbl_username.grid(row=1, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_username = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_username.grid(row=1, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)

        self.lbl_password = tk.Label(
            self, height=1, text="Password:", width=20, justify="left", font=style.label_font, anchor=tk.E)
        self.lbl_password.grid(row=2, column=0, sticky=tk.E,
                               padx=10, pady=0, columnspan=1)
        self.txt_password = tk.Text(self, width=48, height=1, bg="#FFFFFF")
        self.txt_password.grid(row=2, column=1, sticky=tk.W,
                               padx=10, pady=10, columnspan=3)

        self.btn_back = tk.Button(
            self, text="Back to\nlog in", width=10, height=2)
        self.btn_back.grid(row=3, column=2, sticky=tk.W,
                           padx=10, pady=10, columnspan=1)
        self.btn_signup = tk.Button(
            self, text="Sign up", width=10, height=2)
        self.btn_signup.grid(row=3, column=1, sticky=tk.E,
                             padx=10, pady=10, columnspan=1)

    def get_info(self):
        usr = self.txt_username.get("1.0", tk.END).strip('\n')
        pas = self.txt_password.get("1.0", tk.END).strip('\n')
        num = self.txt_phone.get("1.0", tk.END).strip('\n')
        return usr, pas, num
