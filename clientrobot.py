#
# Auteur : ReturnToMonke inc
# Copyright 2021 tous droits réservés
# Reject Humanity tm
#

import socket
import time
import sys
import threading
import re

# test
HOST = '192.168.1.61'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
conn = None

ROBOT_HOST = ''
ROBOT_PORT = 10223
conn_robot = None

in_movement = False

IN_BYTE_MAX_SIZE = 1024
ROBOT_BUFFER_REFRESH_TIME = 10 / 1000 #s


class Protocol:
    forward = "forward"
    backward = "backward"
    left = "left"
    right = "right"
    speed = "speed"
    move_command = [forward, backward, left, right]

    register = "register"

STOP_MOVEMENT = b"DS"
STOP_TURNING = b"TS"

regex_speed = re.compile(rf"{Protocol.speed} (\d)+")


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


def stop():
    global conn_robot
    
    conn_robot.sendall(STOP_MOVEMENT)
    conn_robot.sendall(STOP_TURNING)

def wait_for_input():
    global last_move_command
    global conn, conn_robot
    global in_movement
    global callback_timer

    conn.settimeout(0.1)
    
    while True:

        try:
            data = decode_byte_to_str(conn.recv(IN_BYTE_MAX_SIZE))
        except:
            data = None
        
        if not data:
            if in_movement:
                in_movement = False
                conn_robot.sendall(STOP_MOVEMENT)
                conn_robot.sendall(STOP_TURNING)
        elif data in Protocol.move_command:
            #print("")
            in_movement = True
            conn_robot.sendall(data.encode())
        elif regex_speed.match(data):
            print(f"Change speed to {data}")
            conn_robot.sendall(data.encode())
        else:
            print(f"Not recognized : {data}")
            pass


def main():
    global conn
    global conn_robot

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
    print(f"Connected at local server")
    
    print(f"Connecting to server at {HOST}:{PORT}")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.sendall(f"{Protocol.register} {robotname}".encode())
    data = conn.recv(IN_BYTE_MAX_SIZE).decode("utf-8")
    print(f"Server response : {data}")

    wait_for_input()



main()