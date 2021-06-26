import socket
import pickle
from movement import Movement

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.221"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.Movement = self.connect()

    def getBoard(self):
        return self.Movement

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(8192))
            #return pickle.loads(self.client.recv(2048))
            #temp = pickle.loads(self.client.recv(2048))

        except:
            pass

    def send(self, data):
        try:
            #self.client.send(str.encode(data))
            self.client.send(pickle.dumps(data))
            temp = pickle.loads(self.client.recv(8192))
            return temp
#            return pickle.loads(self.client.recv(8192))
        except socket.error as e:
            print(e)
