import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# from database import DataBase

""" --- manager book and account for server ---"""
class Manager:
    def __init__(self, root = None, database = None):
        self.manager = tk.Toplevel(root)
        self.db = database
        #self.manager.geometry("900x700")
        self.manager.title("Server book manager - Online Library Sever")
        self.manager.spacer = tk.Label(self.manager, height = 4, width = 5, anchor = tk.E)
        self.manager.btn_insert = tk.Button(self.manager, text = "ADD", width = 8, height = 1, font = "Consolas 16 bold", 
                                            command = self.insert_new_book)
        self.manager.btn_update = tk.Button(self.manager, text = "UPDATE", width = 8, height = 1, font = "Consolas 16 bold",
                                            command = self.update_book)
        self.manager.btn_view = tk.Button(self.manager, text = "VIEW", width = 8, height = 1, font = "Consolas 16 bold",
                                            command = self.view_library_book)
        ## Initialize result table
        self.cols_book = ("ID", "Title", "Author", "Published year", "Type", "Link")
        self.cols_width_book = (80, 250, 160, 100, 100, 200)
        self.cols_account = ("Username", "Password")
        self.manager.result = ttk.Treeview(self.manager, columns = self.cols_book, height = 25, show = "headings")
        self.manager.scroll_bar = ttk.Scrollbar(self.manager, command = self.manager.result.yview)
        self.manager.result.configure(yscrollcommand = self.manager.scroll_bar.set)

        for i in range(len(self.cols_book)):
            col = self.cols_book[i]
            width = self.cols_width_book[i]
            self.manager.result.heading(col, text = col)
            self.manager.result.column(col, width = width)

        # Draw widgets
        self.manager.btn_insert.grid(column = 1, row = 0, sticky = "w", padx = 10, pady = 20, columnspan = 2)
        self.manager.btn_update.grid(column = 2, row = 0, sticky = "n", padx = 10, pady = 20, columnspan = 2)
        self.manager.btn_view.grid(column = 4, row = 0, sticky = "w", padx = 10, pady = 20, columnspan = 2)
        self.manager.result.grid(column = 0, row = 2, sticky = 'nsew', pady = 30, columnspan = len(self.cols_book))
        self.manager.scroll_bar.grid(column = len(self.cols_book), row = 2, columnspan = 1)
        # setup button function

    def view_library_book(self, event = None):
        book_list = self.db.get_all_book()
        for rowid in self.manager.result.get_children():
            self.manager.result.delete(rowid)
        for row in book_list:
            self.manager.result.insert("", "end", values = row)
    
    def create_input_box(self):
        self.input_box = tk.Toplevel(self.manager)
        self.input_box.title("Insert book")
        self.input_box.lbl_notice = tk.Label(self.input_box, text = "", font = "Consolas 14")
        self.input_box.lbl = [None] * len(self.cols_book)
        self.input_box.ety = [None] * len(self.cols_book)
        for idx in range(len(self.cols_book)):
            self.input_box.lbl[idx] = tk.Label(self.input_box, text = self.cols_book[idx], font = "Consolas 14 bold")
            self.input_box.ety[idx] = tk.Entry(self.input_box, bd = 2, width = 60 if idx != 5 else 52 , font = "Consolas 14")
            self.input_box.lbl[idx].grid(row = idx, column = 0, padx = 10, pady = 10, sticky = "w")
            self.input_box.ety[idx].grid(row = idx, column = 1, padx = 5, sticky = "w")
        self.input_box.btn_browser = tk.Button(self.input_box, text = "Browser...", command = self.fileDialog)
        self.input_box.btn_insert = tk.Button(self.input_box, text = "INSERT", font = "Consolas 20 bold", command = self.on_insert)
        self.input_box.btn_clear = tk.Button(self.input_box, text = "CLEAR", font = "Consolas 20 bold", command = self.on_clear)

        self.input_box.lbl_notice.grid(row = len(self.cols_book), column = 0, columnspan  = 3, sticky = "n")

        self.input_box.btn_browser.grid(row = 5, column = 1, padx = 5, sticky = "e")
        self.input_box.btn_insert.grid(row = len(self.cols_book) + 1, column = 1, pady = 20, sticky = "w", columnspan = 1)
        self.input_box.btn_clear.grid(row = len(self.cols_book) + 1, column = 1, pady = 20, padx = 150, sticky = "e", columnspan = 1)

    def fileDialog(self, event = None):
        filename = filedialog.askopenfilename(parent = self.input_box, title = "Select a book file")
        if not filename: return
        cwd = os.getcwd()
        if cwd[0] == filename[0] and os.path.commonpath([cwd, filename]) == cwd:
            filename = os.path.relpath(filename, cwd)
        self.input_box.ety[5].delete(0, tk.END)
        self.input_box.ety[5].insert(0, filename)

    def insert_new_book(self, event = None):
        self.manager.btn_insert.config(state = 'disable')
        self.manager.btn_update.config(state = 'disable')
        self.create_input_box()
        def quit_win():
            self.input_box.destroy()
            self.manager.btn_insert.config(state = 'normal')
            self.manager.btn_update.config(state = 'normal')
        self.input_box.protocol("WM_DELETE_WINDOW", quit_win)

    def update_book(self):
        self.manager.btn_insert.config(state = 'disable')
        self.manager.btn_update.config(state = 'disable')
        self.create_input_box()
        self.input_box.btn_insert.configure(text = "UPDATE BOOK", command = self.on_update)
        self.input_box.btn_clear.configure(text = "DELETE BOOK", command = self.on_delete)
        self.input_box.ety[0].configure(width = 52)
        self.input_box.btn_check = tk.Button(self.input_box, text = "GET BOOK", command = self.on_get_book)
        self.input_box.btn_check.grid(row = 0, column = 1, padx = 5, sticky = "e")

        self.reset_update_book()
        def quit_win():
            self.input_box.destroy()
            self.manager.btn_insert.config(state = 'normal')
            self.manager.btn_update.config(state = 'normal')
        self.input_box.protocol("WM_DELETE_WINDOW", quit_win)

    def reset_update_book(self):
        self.input_box.btn_check.configure(text = "GET BOOK")
        self.input_box.lbl_notice.configure(text = '')
        self.input_box.ety[0]['state'] = 'normal'
        for entry in self.input_box.ety[1:]:
            entry.delete(0, tk.END)
            entry['state'] = 'disable'


    def on_clear(self, event = None):
        self.input_box.lbl_notice.configure(text = '')
        for entry in self.input_box.ety:
            entry.delete(0, tk.END)

    def get_book_data(self):
        lst = []
        for idx in range(len(self.cols_book)):
            entry_text = self.input_box.ety[idx].get().strip()
            col = self.cols_book[idx]
            self.input_box.lbl_notice.configure(fg = "red") # set red color error
            if not entry_text:
                self.input_box.lbl_notice.configure(text = "Please enter " + col)
                return
            if (col == "Published year"):
                if (len(entry_text) != 4) or (not entry_text.isdigit()): 
                    self.input_box.lbl_notice.configure(text = "Please enter correct year's format\n(ex: 2020, 1900, ...)")
                    return
            if (col == "ID"):
                if (len(entry_text) > 5):
                    self.input_box.lbl_notice.configure(text = "Please enter Book ID no more than 5 character\n(ex: CS001, 12345,...)")
                    return
                entry_text = entry_text.upper()
            lst.append(entry_text.replace("'", "''")) #replace to avoid ' character cause sql query error
        return tuple(lst)


    def on_insert(self, event = None):
        lst = self.get_book_data()
        if not lst: return
        if self.db.insert_new_book(lst):
            self.input_box.lbl_notice.configure(fg = "green") # successfully
            self.input_box.lbl_notice.configure(text = "Insert book successfully")
            self.manager.result.insert("", "end", values = lst)
        else:
            self.input_box.lbl_notice.configure(fg = "red") # successfull
            self.input_box.lbl_notice.configure(text = "!!! Book ID already exists !!!")


    def on_get_book(self, event = None):
        if self.input_box.btn_check['text'] == 'CLOSE BOOK':
            self.reset_update_book()
            return
        else: # if click on GET BOOK
            ID = self.input_box.ety[0].get()
            book = self.db.get_one_book(ID)
            if not book: return
            book = book[0]
            for i in range(1, len(self.cols_book)):
                self.input_box.ety[i]['state'] = 'normal'
                self.input_box.ety[i].delete(0, tk.END)
                self.input_box.ety[i].insert(0, book[i])
            self.input_box.ety[0]['state'] = 'disabled'
            self.input_box.btn_check.configure(text = "CLOSE BOOK")

    def on_delete(self, event = None):
        if self.input_box.ety[1]['state'] != 'normal': #if not found this book id
            return
        ID = self.input_box.ety[0].get()
        self.db.delete_one_book(ID)
        self.reset_update_book()
        self.input_box.lbl_notice.configure(text = "Delete book successfully", fg = "green")

    def on_update(self, event = None):
        if self.input_box.ety[1]['state'] != 'normal': #if not found this book id
            return
        book = self.get_book_data()
        if not book: return
        self.db.update_one_book(book)
        self.input_box.lbl_notice.configure(text = "Update book successfully", fg = "green")

    
    def run(self):
        self.manager.mainloop()

