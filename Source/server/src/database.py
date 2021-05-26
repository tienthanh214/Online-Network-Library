import sqlite3

class DataBase:
    def __init__(self, link = 'assets/library.db'):
        self.link = link
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        # Creat table
        ## Creat table Book
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS BOOK (
                ID NCHAR(5) PRIMARY KEY,
                Name NVARCHAR(50),
                Author NVARCHAR(30),
                PublishYear YEAR,
                Type NVARCHAR(30),
                Link NVARCHAR(40)
            )
        """)
        ## Creat table Account
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS ACCOUNT (
                Username VARCHAR(30) PRIMARY KEY,
                Password VARCHAR(30)
            )
        """)
        # self.cur.execute("INSERT INTO BOOK VALUES ('CS001', 'Computer Science An overview', 'Brookshear & Brylow', 1985, 'Computer Science', 'assets/books/book1.txt')")
        # self.cur.execute("INSERT INTO BOOK VALUES ('NV001', 'The Alchemist', 'Paulo Coelho', 1988, 'Novel', 'assets/books/book2.txt')")
        # self.cur.execute("INSERT INTO BOOK VALUES ('SK001', 'Time management', 'Lorem', 2020, 'Soft Skill', 'assets/books/book3.txt')")
        # self.conn.commit()
        # self.cur.execute("INSERT INTO ACCOUNT VALUES ('tienthanh214', '2142001')")
        # self.cur.execute("INSERT INTO ACCOUNT VALUES ('lecongbinh', '123456')")
        # self.cur.execute("INSERT INTO ACCOUNT VALUES ('a', 'a')")
        # self.conn.commit()
        self.cur.close()
        self.conn.close()

    @staticmethod
    def standardized_input(x):
        x = str(x)
        if x.find('"') != -1: # if have " string format will be '...'
            return x.replace('"', '""')
        else:
            return x.repace("'", "''")

    def book_query(self, query):
        if len(query.split(maxsplit = 1)) != 2: # invalid query
            return []
        qtype, param = query.split(maxsplit = 1)
        qtype = qtype[2:].upper()
        param = param.upper()
        if (qtype == 'ID'): param = "'" + param + "'"
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("SELECT ID, Name, Author, PublishYear, Type FROM BOOK WHERE UPPER(" + qtype + ") = " + param)
        except:
            return []
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def get_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT Link FROM BOOK WHERE ID = '%s'" % ID)
        link = self.cur.fetchall()[0][0]
        fi = open(link, 'r', encoding = 'utf8')
        content = fi.read()
        fi.close()
        self.cur.close()
        self.conn.close()
        return content

    def account_sign_up(self, username, password):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()

        self.cur.execute("""SELECT username FROM ACCOUNT WHERE username = '%s'""" % username)
        if (not self.cur.fetchall()):
            self.cur.execute("""INSERT INTO ACCOUNT VALUES ('%s', '%s')""" % (username, password.replace("\\'", "''")))
            self.conn.commit()
            msg = "SUCCESS"
        else:
            msg =  "FAIL Username already exists"

        self.cur.close()
        self.conn.close()
        return msg

    def account_sign_in(self, username, password):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT username, password FROM ACCOUNT WHERE username = '%s'" % username)
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        if (result):
            if (result[0][1] == password):
                return "SUCCESS"
            else:
                return "FAIL Incorrect password"
        else:
            return "FAIL Invalid account"


    # extension for server book manager
    def get_all_book(self):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * from BOOK")
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result
    
    def get_one_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * from BOOK where ID = '%s'" % ID.upper())
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def insert_new_book(self, book):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT ID FROM BOOK WHERE ID = '%s'""" % book[0].upper())
        flag = False
        if not self.cur.fetchall(): # if ID not already exists
            self.cur.execute("""INSERT INTO BOOK VALUES """ + str(book))
            self.conn.commit()
            flag = True
        self.cur.close()
        self.conn.close()
        return flag    
    
    def delete_one_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("""DELETE FROM BOOK WHERE ID = '%s'""" % ID.upper())
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def update_one_book(self, book):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("""DELETE FROM BOOK WHERE ID = '%s'""" % book[0])
        self.cur.execute("""INSERT INTO BOOK VALUES """ + str(book).replace("\\'", "''"))
        self.conn.commit()
        self.cur.close()
        self.conn.close()