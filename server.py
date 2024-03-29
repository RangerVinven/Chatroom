import socket
import multiprocessing
from Classes.Chatroom import Chatroom

rooms = [
    Chatroom("Shuang"),
    Chatroom("Azam"),
    Chatroom("Ian"),
    Chatroom("Paul"),
    Chatroom("Chrissy")
]

# This project works in a couple steps:
# 1. The chatroom "manager" runs server.py
# 2. The server creates some chatrooms by default. All of which listen on a random port
# 3. server.py listens for connections at port 9999
# 4. When someone connects (the client) to port 9999, server.py sends a welcome message and the different chatrooms
# 5. The client sends their chatroom of choice
# 6. The server sends back the port number of that chatroom
# 7. The client disconnects from port 9999 and reconnects with that port
# 8. The client is able to send messages to the chatroom
# 9. The chatroom is always listening for messages. When it recieves one, it sends it to all the connected users 

def get_user_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        try:
            # Listens on port 9999
            soc.bind(("127.0.0.1", 9999))
            soc.listen(10)

            while True:

                # Accepts connections and sends the welcome message
                connection, address =  soc.accept()
                connection.sendall(b"Welcome to the Awesome Chatroom Server! Which server would you like to join?\n")

                # Gets a list of the chatrooms
                room_names = []
                rooms_list = ""
                for room in rooms:
                    rooms_list = rooms_list + room.getRoomName() + "\n"
                    room_names.append(room.getRoomName())

                # Sends the list of the chatrooms
                connection.sendall(rooms_list.encode("utf-8"))

                # Receives the user's chatroom choice
                user_choice = connection.recv(1024).decode()

                # Sends the port of the chosen chatroom
                for room in rooms:
                    if(room.getRoomName() == user_choice):
                        connection.sendall(str(room.getPort()).encode("utf-8"))

        except Exception as e:
            print(e)
            soc.close()
    
# Gives the user managment options for the server and starts the listening thread
def start_server():
    try:

        # Starts a thread running get_user_connections
        server_process = multiprocessing.Process(target=get_user_connections)
        server_process.start()

        while True:
            print('''
        [1] List all rooms
        [2] Create a room
        [3] Delete a room
        [4] Shutdown server
                ''')
            
            # Gets the user's option
            selected_option = input("Please enter your option: ")
            while selected_option not in ["1", "2", "3", "4"]:
                selected_option = input("Please enter your option: ")

            selected_option = int(selected_option)

            # List rooms
            if(selected_option == 1):
                if len(rooms) == 0:
                    print("There aren't any rooms")
                
                else:
                    for room in rooms:
                        print("{} - {}".format(room.getRoomName(), room.getPort()))

            # Create room
            elif(selected_option == 2):
                room_name = input("What's the new room's name: ")
                rooms.append(Chatroom(room_name))

            # Delete room
            elif(selected_option == 3):
                room_to_delete = input("Enter the name of the room you want deleted: ")
                original_length = len(rooms)

                # Deletes the selected room
                for i in range(len(rooms)):
                    if rooms[i].getRoomName() == room_to_delete:
                        
                        # Deletes the chatroom
                        rooms[i].closeChatroom()
                        rooms.pop(i)

                        print("Room deleted")
                        break

                if len(rooms) == original_length:
                    print("No rooms deleted")

            # Shutdown server
            else:
                close_chatrooms()

                print("Connection closed. Goodbye :)")

                server_process.terminate()
                exit()

    except Exception as e:
        close_chatrooms()
        server_process.terminate()
        exit()

# Closes all the chatrooms
def close_chatrooms():
    for room in rooms:
        room.closeChatroom()

if __name__ == "__main__":
    start_server()