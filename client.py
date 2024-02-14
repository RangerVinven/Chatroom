import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    try:
        soc.connect(("127.0.0.1", "9999"))


    except Exception as e:
        print(e)
        soc.close()