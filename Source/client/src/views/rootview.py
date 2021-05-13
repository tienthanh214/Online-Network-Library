import tkinter as tk
from tkinter import font as tkfont

from login import Login
from signup import Signup
from connect import Connect
from search import Search
from book import Book

class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # predefined fonts for UI consistency
        self.title_font = tkfont.Font(
            family='Helvetica', size=12, weight="bold", slant="roman")
        self.label_font = tkfont.Font(
            family='Helvetica', size=10, weight="bold", slant="roman")
        self.user_font = tkfont.Font(
            family='Helvetica', size=14, weight="normal", slant="italic")

        # use tkraise to show frame above the other
        self.container = tk.Frame(self)
        self.geometry("768x560+50+50")
        self.title("Online Library")
        self.resizable(False, False)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.grid()

        self.username = "<N/A>"

        self.frames = {}
        for F in (Login, Signup, Connect, Search):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # for testing only
        self.show_frame("Search")
        # self.frames["Search"].show_result([["spam", 42, "test", ""],["eggs", 451, "", "we"],["spam", 42, "test", ""],["eggs", 451, "", "we"],["spam", 42, "test", ""],["eggs", 451, "", "we"],["spam", 42, "test", ""],["eggs", 451, "", "we"],["spam", 42, "test", ""],["eggs", 451, "", "we"],["bacon", "True", "", ""]])

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is the start page", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)

#         button1 = tk.Button(self, text="Go to Page One",
#                             command=lambda: controller.show_frame("PageOne"))
#         button2 = tk.Button(self, text="Go to Page Two",
#                             command=lambda: controller.show_frame("PageTwo"))
#         button1.pack()
#         button2.pack()

# self.book = Book(tk.Toplevel(self), 'eed', 'frfr')
# self.book.mainloop()

if __name__ == "__main__":
    app = RootView()
    app.mainloop()
