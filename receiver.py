import sublime
import sublime_plugin
import socket
import json

def get_scripts():
    # its like poking a bear | poke = message | bear == addr
    # will return scripts 

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 39999        # The port used by the server

    data = json.dumps({"messageID":0})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data.encode("UTF-8"))
        print("sent it")
        # data = s.recv(1024)

    # print('Received', repr(data))
    full_data = ""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        print("listening")
        c.bind((HOST, 39998))
        c.listen(1)
        conn, addr = c.accept()
        with conn:
            print("connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                full_data += data.decode("UTF-8")
    print(json.dumps(full_data, indent=4))

# get_scripts()

