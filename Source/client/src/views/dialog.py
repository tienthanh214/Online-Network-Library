import tkinter as tk


def messagebox(title="Online Library", msg="Something is wrong :(", type="warn"):
    # type are: warn, error, info
    title = title.capitalize()
    if type == "error":
        tk.messagebox.showerror(title, msg)
    elif type == "warn":
        tk.messagebox.showwarning(title, msg)
    else:
        tk.messagebox.showinfo(title, msg)
