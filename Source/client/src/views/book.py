import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import src.views.textstyles as style


class Book(tk.Frame):
    def __init__(self, parent, bookid, title, content, sendfunc):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("View Book")
        self.parent.resizable(False, False)
        self._bookid = bookid
        self._title = title
        self._content = content
        self._sendfunc = sendfunc
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        self.lbl_title = tk.Label(self.parent, text=self._title, width=24, justify="center",
                                  font=style.title_font, wraplength=360, bg='#fc9d9a', fg='#aa2e00')
        self.lbl_title.grid(row=0, column=0, sticky=tk.S+tk.N,
                            padx=10, pady=10, columnspan=4)

        self.txt_content = scrolledtext.ScrolledText(
            self.parent, width=64, height=20, bg="#FFFFFF")
        self.txt_content.insert("end", self._content)
        self.txt_content.configure(state="disable")
        self.txt_content.grid(row=1, column=0, sticky=tk.N,
                              padx=10, pady=10, columnspan=4)

        self.btn_clear = tk.Button(self.parent, text="Download", width=10, height=1, command=self.download_book,
                                   font=style.btn_font, bg=style.btn_style['bg'], fg=style.btn_style['fg'])
        self.btn_clear.grid(row=2, column=3, sticky=tk.S+tk.E,
                            padx=10, pady=10, columnspan=1)

    def download_book(self):
        self._sendfunc(self._bookid)
        files = [('Text Document', '*.txt')]
        file = filedialog.asksaveasfile(
            mode="wb", initialfile=self._title, filetypes=files, defaultextension=files, title="Save Book")
        if file != None:
            file.write(self._content.encode("utf8"))
            file.close()
