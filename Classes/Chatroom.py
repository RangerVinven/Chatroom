import socket
import threading
import time
from random import randint

class Chatroom:
    def __init__(self, room_name):
        # Assigns itself a port
        port = randint(1000, 10000)
        while port == 9999:
            port = randint(1000, 10000)

        # Defines necessary variables
        self.room_name = room_name
        self.clients = []
        self.port = port
        self.is_running = True

        # Starts listening for connections
        self.server_thread = threading.Thread(target=self.startServer)
        self.server_thread.start()

    # Listens and accepts connections
    def startServer(self):

        # Starts listening for connections
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(("127.0.0.1", self.port))
        self.soc.listen(10)

        while self.is_running:

            try:
                # Constantly accepts connections
                connection, address = self.soc.accept()
                current_time = int(time.time())

                # Adds the new connections to the clients array
                self.clients.append((connection, address, current_time))

                # Sends the welcome message
                connection.sendall("You've connected to {}! Welcome!\n".format(self.room_name).encode("utf-8"))

                # Listens for messages from the newly connected user
                threading.Thread(target=self.listen_for_messages, args=(connection,current_time)).start()

            except OSError:
                return
        else:
            return

    # Loops and broadcasts messages to all the connected users
    def listen_for_messages(self, connection, id):
        while self.is_running:
            try:
                # Receives the user's message
                user_message = connection.recv(1024)
                
                # Sends the message to all the clients
                for client in self.clients:
                    client[0].sendall(user_message) # client is a tuple of (connection, address, id) 
            
            # If the user closes the program
            except ConnectionResetError:

                # Loops through the clients array 
                for i in range(len(self.clients) - 1):
                    
                    # Disconnects the user
                    if(self.clients[i][2] == id):
                        self.clients.pop(i)
                        break

                break
        
        else:
            return

    def getClients(self):
        return self.clients
    
    def getRoomName(self):
        return self.room_name
    
    def getPort(self):
        return self.port
    
    # Shutsdown the chatroom
    def closeChatroom(self):
        self.is_running = False

        # Disconnects the clients
        for client in self.clients:
            print("Sending shutdown")
            client[0].sendall(b"SERVER-SHUTDOWN")
            client[0].close()

        # Closes the port
        self.soc.close()