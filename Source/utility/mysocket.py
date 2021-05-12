import socket as sk
import struct as stc


class MySocket:
    def __init__(self, sock=None):
        super().__init__()
        if sock == None:
            self._reset()
            self._currentip = 0
        else:
            self._isconnected = True
            self._sock = sock

    def _reset(self):
        self._isconnected = False
        self._sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def connect(self, ip, port=54321):
        self._isconnected = True
        try:
            self._currentip = ip
            address = (ip, port)
            self._sock.connect(address)
        except:
            self._reset()

    def send(self, msg):
        """Prefix each message with a 4-byte length (network byte order)"""
        msg = stc.pack('>I', len(msg)) + msg
        print("> send len: ", len(msg))
        self._sock.sendall(msg)

    def receive(self):
        """Read message length and unpack it into an integer"""
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = stc.unpack('>I', raw_msglen)[0]
        print("> recv len: ", msglen)
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        """Helper function to recv n bytes or return None if EOF is hit"""
        data = bytearray()
        while len(data) < n:
            packet = self._sock.recv(n - len(data))
            if not packet:
                break
            if not packet == None:
                data.extend(packet)
        return data

    def close(self):
        # Close the socket file descriptor
        # Both sends and receives are disallowed
        self._sock.close()
        self._reset()

    def shutdown(self):
        # Shutdown one halves of the connection
        # Further sends are disallowed
        self._sock.shutdown(sk.SHUT_WR)
        self._reset()
