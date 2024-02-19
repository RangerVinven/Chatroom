import socket
import threading

def connect_to_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connects to the server
        soc.connect(("127.0.0.1", 9999))

        # Receives the welcome message
        welcome_message = soc.recv(1024).decode()
        print(welcome_message)

        # Receives the list of chatrooms
        chatrooms = soc.recv(1024).decode()
        print(chatrooms)

        # Sends the chatroom's name
        chatroom_to_join = input("Please enter the name of the room you wish to join: ")
        soc.sendall(chatroom_to_join.encode("utf-8"))

        # Receives the port of the chatroom
        port = soc.recv(1024).decode()

        # Disconnects from the server and reconnects to the chatroom
        try:
            soc.close()

        except Exception as e:
            print(e)

        else:
            connect_to_chatroom(int(port))

    except Exception as e:
        print(e)
        soc.close()

def connect_to_chatroom(port):
    username = input("What do you want your username to be: ")

    # Connects to the chatroom
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("127.0.0.1", port))

    # Receives and displays the welcome message
    welcome_message = soc.recv(1024).decode()
    print(welcome_message)

    # Starts a thread that listens for new messages
    threading.Thread(target=receive_messages, args=(soc,username)).start()

    # Loops and allows the user to send messages
    while True:
        message = input()

        if message not in ["!HELP", "!DISCONNECT", "!EXIT"]:
            message = username + ": " + message
            soc.sendall(message.encode("utf-8"))

        else:
            run_command(message, soc)

# Runs a command
def run_command(message, soc):
    if message == "!HELP":
        print('''
!DISCONNECT - disconnects from the chatroom. Takes you back to the main menu.
!EXIT - exits the program
''')

        
    elif message == "!DISCONNECT":
        soc.close()
        connect_to_server()
    
    else:
        soc.close()
        exit()


def receive_messages(soc, username):
    while True:
        try:
            message = soc.recv(1024).decode()

            # Closes the program if the server shutdown
            # If a user sends SERVER-SHUTDOWN, it'll send as username: SERVER-SHUTDOWN, therefore not triggering this statement
            if message == "SERVER-SHUTDOWN":
                print("Server shutdown")
                break

            # Only prints if the message is from another user
            if not (message.split(":")[0] == username):
                print(message)

        except ConnectionAbortedError:
            break

        except ConnectionResetError:
            break
    
    exit()

if __name__ == "__main__":
    connect_to_server()