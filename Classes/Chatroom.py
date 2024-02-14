import socket
import threading
import time
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
            current_time = int(time.time())
            self.clients.append((connection, address, current_time))

            connection.sendall("You've connected to {}! Welcome!\n".format(self.room_name).encode("utf-8"))

            threading.Thread(target=self.listen_for_messages, args=(connection,current_time)).start()

    def listen_for_messages(self, connection, id):
        while True:
            try:
                user_message = connection.recv(1024)
                
                # Sends the message to all the clients
                for client in self.clients:
                    # client is a tuple of (connection, address)
                    client[0].sendall(user_message)
            
            # If the user closes the program
            except ConnectionResetError:
                # Removes the client from the clients array
                for i in range(len(self.clients) - 1):
                    if(self.clients[i][2] == id):
                        self.clients.pop(i)
                        break

                break

    def getClients(self):
        return self.clients
    
    def getRoomName(self):
        return self.room_name
    
    def getPort(self):
        return self.port
    
    def closeChatroom(self):
        self.soc.close()