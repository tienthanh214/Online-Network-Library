# import sys
# sys.path.insert(0, '../utility')
# import mysocket as msk

# import socket as sk
# from threading import Thread

# def accept_incoming_connections():
#     """Sets up handling for incoming clients."""
#     while True:
#         client, client_address = SERVER._sock.accept()
#         myclient = msk.MySocket(sock=client)
#         print("> %s:%s has connected." % client_address)
#         addresses[client] = client_address
#         Thread(target=handle_client, args=(myclient,)).start()


# def handle_client(client):  # Takes client socket as argument.
#     """Handles a single client connection."""
#     #clients[client] = name

#     while True:
#         req = client.receive().decode("utf8")
#         print("> request: %s" % req)
#         if req != bytes("{quit}", "utf8"):
#             book = open("./assets/books/book1.txt", "rb")
#             client.send(msg=book.read())
#         else:
#             client.send(bytes("{quit}", "utf8"))
#             client.close()
#             # del clients[client]
#             break


# # def broadcast(msg, prefix=""):  # prefix is for name identification.
# #     """Broadcasts a message to all the clients."""

# #     for sock in clients:
# #         send_msg(sock, bytes(prefix, "utf8")+msg)

        
# clients = {}
# addresses = {}

# HOST = ''
# PORT = 33000
# BUFSIZ = 1024
# ADDR = (HOST, PORT)

# SERVER = msk.MySocket()
# SERVER._sock.bind(ADDR)

# if __name__ == "__main__":
#     SERVER._sock.listen(5)
#     print("Waiting for connection...")
#     ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
#     ACCEPT_THREAD.start()
#     ACCEPT_THREAD.join()
#     SERVER.close()
