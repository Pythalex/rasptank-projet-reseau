#
# Auteur : ReturnToMonke inc
# Copyright 2021 tous droits réservés
# Reject Humanity tm
#

import socket
import time
import sys


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
conn = None

ROBOT_HOST = ''
ROBOT_PORT = 10223
conn_robot = None

IN_BYTE_MAX_SIZE = 1024
ROBOT_BUFFER_REFRESH_TIME = 10 #ms

class Protocol:
    forward = "forward"
    backward = "backward"
    left = "left"
    right = "right"
    speed = "speed 100"
    move_command = [forward, backward, left, right]

    register = "register"
    

key_binding = {
    "forward" : "forward"
}

def decode_byte_to_str(b):
    try:
        decoded = b.decode("utf-8")
        return decoded
    except:
        print(f"[THREAD] Error when decoding input byte as utf-8: {b}")
        return None


def recv_wait(conn):
    while True:
        data = decode_byte_to_str(conn.recv(IN_BYTE_MAX_SIZE))
        if not data:
            time.sleep(ROBOT_BUFFER_REFRESH_TIME)
        else:
            return data


def wait_for_input():
    while True:
        data = recv_wait(conn)
        if data in Protocol.move_command:
            print("Implement move")
        elif data == Protocol.speed:
            print("Implement speed")
        else:
            print(f"Command '{data}' not understood")


def main():
    global conn
    global HOST
    global PORT

    print("=================================")
    print("=     CLIENT  ROBOTSWAG         =")
    print("=  Copyright© ReturnToMonke inc =")
    print("=  2021                         =")
    print("=================================")

    print("python3 clientrobot.py [robotname] [hostip] [hostport]")

    robotname = "robotswag"

    if len(sys.argv) > 1:
        robotname = sys.argv[1]
    if len(sys.argv) > 2:
        HOST = sys.argv[2]
    if len(sys.argv) > 3:
        PORT = sys.argv[3]

    print(f"This robot will have name {robotname}")

    print(f"Connecting to robot server at {ROBOT_HOST}:{ROBOT_PORT}")
    conn_robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_robot.connect((ROBOT_HOST, ROBOT_PORT))

    print(f"Connecting to server at {HOST}:{PORT}")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.sendall(f"{Protocol.register} {robotname}".encode())
    data = conn.recv(IN_BYTE_MAX_SIZE).decode("utf-8")
    print(f"Server response : {data}")

    wait_for_input()



main()