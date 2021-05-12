import socket as sk
import struct as stc

class MySocket(sk.socket):
    def __init__(self):
        super().__init__()
        
    def _reset(self):
        self._isconnected = False
        self._sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def accept(self):
        con, addr = sk.socket.accept(self)
        return self.__class__(con), addr

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


