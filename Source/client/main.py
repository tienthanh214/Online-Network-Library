# #!/usr/bin/env python3
# """Script for Tkinter GUI chat client."""
# #https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
# from socket import AF_INET, socket, SOCK_STREAM
# import sys
# sys.path.insert(0, '../utility')
# import mysocket as msk
# from threading import Thread
# import tkinter


# def receive():
#     """Handles receiving of messages."""
#     while True:
#         try:
#             msg = client_socket.receive().decode("utf8")
#             msg_list.insert(tkinter.END, msg)
#         except OSError:  # Possibly client has left the chat.
#             break


# def send(event=None):  # event is passed by binders.
#     """Handles sending of messages."""
#     msg = my_msg.get()
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#         top.quit()


# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
#     send()

# top = tkinter.Tk()
# top.title("Book reader")

# messages_frame = tkinter.Frame(top)
# my_msg = tkinter.StringVar()  # For the messages to be sent.
# my_msg.set("Type your messages here.")
# scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# # Following will contain the messages.
# msg_list = tkinter.Text(top, height=20, width=60)
# msg_list.pack()
# messages_frame.pack()

# entry_field = tkinter.Entry(top, textvariable=my_msg)
# entry_field.bind("<Return>", send)
# entry_field.pack()
# send_button = tkinter.Button(top, text="Send", command=send)
# send_button.pack()

# top.protocol("WM_DELETE_WINDOW", on_closing)

# #----Now comes the sockets part----
# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)

# BUFSIZ = 4096
# ADDR = (HOST, PORT)

# client_socket = msk.MySocket()
# client_socket.connect(HOST, PORT)

# receive_thread = Thread(target=receive)
# receive_thread.start()
# tkinter.mainloop()  # Starts GUI execution.
