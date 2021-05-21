import socket
import threading
import sys
import time


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9000        # The port used by the server

IN_BYTE_MAX_SIZE = 1024
ROBOT_BUFFER_REFRESH_TIME = 10 #ms


def decode_byte_to_str(b):
    try:
        decoded = b.decode("utf-8")
        return decoded
    except:
        print(f"[THREAD] Error when decoding input byte as utf-8: {b}")
        return None

def pc():
    print("Yo")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(b"connect robotswag")
    data = s.recv(1024).decode("utf-8")
    print(f"Server : {data}")

    s.sendall(b"forward")

def robot():
    print("Yo")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(b"register robotswag")
     
    data = s.recv(1024).decode("utf-8") 
    print(f"Server : {data}")

    while True:
        time.sleep(10/1000)
        data = s.recv(1024).decode("utf-8")
        if not data:
            continue
        print(f"Received : {data}")


def recv_wait(conn):
    while True:
        data = decode_byte_to_str(conn.recv(IN_BYTE_MAX_SIZE))
        if not data:
            time.sleep(ROBOT_BUFFER_REFRESH_TIME)
        else:
            return data


def main():

    opt = sys.argv[1]

    if opt == "pc":
        t2 = threading.Thread(target=pc)
        t2.start()
        t2.join()
    elif opt == "robot":
        t1 = threading.Thread(target=robot)
        t1.start()
        t1.join()
    else:
        print("What?")

main()