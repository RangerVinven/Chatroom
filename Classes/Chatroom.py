import socket
import threading
from random import randint

class Chatroom:
    def __init__(self, room_name):
        port = randint(1000, 10000)
        while port == 9999:
            port = randint(1000, 10000)

        self.room_name = room_name
        self.clients = []
        self.port = port

        self.server_thread = threading.Thread(target=self.startServer)
        self.server_thread.start()

    def startServer(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(("127.0.0.1", self.port))
        self.soc.listen(10)

        while True:
            connection, address =  self.soc.accept()
            self.clients.append((connection, address))

            connection.sendall("You've connected to {}! Welcome!\n".format(self.room_name).encode("utf-8"))

    def getClients(self):
        return self.clients
    
    def getRoomName(self):
        return self.room_name
    
    def getPort(self):
        return self.port
    
    def closeChatroom(self):
        self.soc.close()