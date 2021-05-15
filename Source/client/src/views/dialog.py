import tkinter as tk


def messagebox(title="Online Library", msg="Something is wrong :(", type="warn"):
    # type are: warn, error, info
    if type == "error":
        tk.messagebox.showerror(title, msg)
    elif type == "warn":
        tk.messagebox.showwarning(title, msg)
    else:
        tk.messagebox.showinfo(title, msg)

def yesno(title="Question", question="Yes or No?"):
    return tk.messagebox.askyesno(title, question)

def isvalid_username(usr):
    '''a-z 1-9'''
    pass

def isvalid_password(pas):
    '''any except \n, \t, space, ', " '''
    pass