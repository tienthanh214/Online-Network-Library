import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = ("192.168.11.1", 54321)
client.connect(IP)

try:
    while True:
        # print(client)
        msg = input('Client: ')
        client.sendall(bytes(msg, "utf8"))
        msg = client.recv(1024)
    # client.sendall(b"This is the message from client")
except KeyboardInterrupt:
    client.sendall(bytes("QUIT", "utf8"))
    client.close()
finally:
    client.close()