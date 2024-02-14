import socket
import threading
from Classes.Chatroom import Chatroom

rooms = [Chatroom("Hello"), Chatroom("World"), Chatroom("Boo"), Chatroom("Test")]

def get_user_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        try:
            # Listens on port 9999
            soc.bind(("127.0.0.1", 9999))
            soc.listen(10)

            while True:

                # Sends the welcome message
                connection, address =  soc.accept()
                connection.sendall(b"Welcome to the Finlay-Daniel Chatroom Server! Which server would you like to join?\n")

                # Gets a list of the chatrooms
                room_names = []
                rooms_list = ""
                for room in rooms:
                    rooms_list = rooms_list + room.getRoomName() + "\n"
                    room_names.append(room.getRoomName())

                # Sends the list of the chatrooms
                connection.sendall(rooms_list.encode("utf-8"))

                # Recieves the user's chatroom choice
                user_choice = connection.recv(1024).decode()

                # Sends a "invalid room" message
                # while user_choice not in room_names:
                #     connection.sendall("That room doesn't exist, please enter a valid option\n".encode("utf-8"))
                #     user_choice = connection.recv(1024).decode()

                # Sends the port of the chosen chatroom
                for room in rooms:
                    if(room.getRoomName() == user_choice):
                        connection.sendall(str(room.getPort()).encode("utf-8"))

                # Disconnects the user
                # connection.close()


        except Exception as e:
            print(e)
            soc.close()
    


try:

    server_thread = threading.Thread(target=get_user_connections)
    server_thread.start()

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
                    rooms[i].closeChatroom()
                    rooms.pop(i)
                    print("Room deleted")

                    break

            if len(rooms) == original_length:
                print("No rooms deleted")

        # Shutdown server
        else:
            for room in rooms:
                room.closeChatroom()

            print("Connection closed. Goodbye :)")
            break

except Exception as e:
    print(e)
    for room in rooms:
        room.closeChatroom()