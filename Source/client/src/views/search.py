import tkinter as tk
from tkinter import ttk


class Search(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self._user = "ded"
        self.create_widgets()

    def create_widgets(self):
        import textstyles as style

        self.lbl_user = tk.Label(
            self, height=1, text=self._user, width=20, justify="right", font=style.user_font, anchor=tk.E)
        self.lbl_user.grid(row=0, column=2, sticky=tk.E,
                           padx=0, pady=10, columnspan=2)
        self.btn_logout = tk.Button(
            self, text="Log out", width=10, height=1)
        self.btn_logout.grid(row=0, column=4, sticky=tk.E,
                             padx=10, pady=10, columnspan=1)

        self.lbl_query = tk.Label(
            self, height=1, text="Query:", width=15, justify="left", anchor=tk.E, font=style.label_font)
        self.lbl_query.grid(row=1, column=0, sticky=tk.W,
                            padx=10, pady=0, columnspan=1)
        self.txt_query = tk.Text(self, width=56, height=1, bg="#FFFFFF")
        self.txt_query.grid(row=1, column=1, sticky=tk.W,
                            padx=10, pady=10, columnspan=2)

        self.btn_search = tk.Button(
            self, text="Search", width=10, height=1)
        self.btn_search.grid(row=1, column=4, sticky=tk.E,
                             padx=10, pady=10, columnspan=1)

        self.lbl_result = tk.Label(
            self, height=1, text="~" * 12 + " Result " + "~" * 12, width=30, font=style.label_font)
        self.lbl_result.grid(row=2, column=1, sticky=tk.W + tk.E,
                             padx=10, pady=0, columnspan=3)
        self.scb_result = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scb_result.grid(
            row=3, column=5, sticky=tk.N+tk.S+tk.W, columnspan=1)
        cols = ("ID", "Title", "Author", "Type")
        self.tbl_result = ttk.Treeview(
            self, columns=cols, show="headings", yscrollcommand=self.scb_result.set, selectmode="browse", height=12)
        self.scb_result.config(command=self.tbl_result.yview)
        self.tbl_result.grid(row=3, column=0, sticky=tk.E,
                             padx=0, pady=10, columnspan=5)
        for col in cols:
            self.tbl_result.heading(col, text=col)
            self.tbl_result.column(col, width=164, stretch=True)
        self.tbl_result.tag_configure('0', background='#E8E8E8')
        self.tbl_result.tag_configure('1', background='#DFDFDF')

        self.btn_clear = tk.Button(
            self, text="Clear", width=6, height=1, command=self.clear_result)
        self.btn_clear.grid(row=4, column=4, sticky=tk.E,
                            padx=10, pady=10, columnspan=1)

    def show_result(self, table):
        self.clear_result()
        for items in table:
            row = (items[0], items[1], items[2], items[3])
            self.tbl_result.insert("", "end", values=row,
                                   tags=(str(items.__index__ % 2)))

    def clear_result(self):
        for rowid in self.tbl_result.get_children():
            self.tbl_result.delete(rowid)

    def get_query(self):
        return self.txt_query.get("1.0", tk.END).strip('\n')

    def get_bookid(self, event):
        curItem = self.tbl_result.focus()
        return self.tbl_result.item(curItem)['values'][0].strip('\n')
