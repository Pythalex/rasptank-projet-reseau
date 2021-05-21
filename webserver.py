#!/usr/bin/env python3

import socket
import threading
import re
import time

HOST = ''  # Standard loopback interface address (localhost)
PORT = 9000        # Port to listen on (non-privileged ports are > 1023)
IN_BYTE_MAX_SIZE = 1024
ROBOT_BUFFER_REFRESH_TIME = 10 / 1000 #ms

pc_to_robot_map = {}
registered_robots = {}
buffer = {}

ROBOT_AVAILABLE = 1
ROBOT_UNAVAILABLE = 2
ROBOT_DEFAULT_MAX_SPEED = 80

class Protocol:
    forward = "forward"
    backward = "backward"
    left = "left"
    right = "right"
    speed = "speed"
    move_command = [forward, backward, left, right]

    connect = "connect"
    register = "register"

    ok = b"ok"
    unknown = b"unknown"
    already_used = b"already_used"


regex_connect = re.compile(rf"{Protocol.connect} (\w+)")
regex_register = re.compile(rf"{Protocol.register} (\w+)")
regex_speed = re.compile(rf"{Protocol.speed} (\d+)")


def decode_byte_to_str(b):
    try:
        decoded = b.decode("utf-8")
        return decoded
    except:
        print(f"[THREAD] Error when decoding input byte as utf-8: {b}")
        return None


def process_input(conn, addr):
    with conn:
        while True:
            data = recv_wait(conn)
            if not data:
                break

            print(f"[THREAD] Received {data}")

            # Message matching
            if regex_connect.match(data):
                robotname = regex_connect.match(data).groups()[0]
                return_data = process_connect(conn, addr, robotname)
            elif regex_register.match(data):
                robotname = regex_register.match(data).groups()[0]
                return_data = process_register(conn, addr, robotname)
            else:
                print("[THREAD] Input not understood.")

            return return_data


def process_register(conn, addr, robotname):
    if not robotname in registered_robots:
        registered_robots[robotname] = ROBOT_AVAILABLE
        conn.sendall(Protocol.ok)
    else:
        conn.sendall(Protocol.already_used)
    print(f"New robot list : {registered_robots}")
    buffer[robotname] = []
    read_input_for_robot(conn, addr, robotname)


def read_input_for_robot(conn, addr, robotname):
     
    while True:
        time.sleep(ROBOT_BUFFER_REFRESH_TIME)
        while len(buffer[robotname]) > 0:
            command = buffer[robotname].pop()
            conn.sendall(command.encode())


def process_connect(conn, addr, robotname):
    if robotname in registered_robots:
        if registered_robots[robotname] == ROBOT_AVAILABLE:
            pc_to_robot_map[(conn, addr)] = robotname
            registered_robots[robotname] = ROBOT_UNAVAILABLE
            conn.sendall(Protocol.ok)
        else:
            conn.sendall(Protocol.already_used)
    else:
        conn.sendall(Protocol.unknown)
    print(f"New mapping : {pc_to_robot_map}")
    wait_input(conn, addr, robotname)


def wait_input(conn, addr, robotname):
    while True:
        #print(f"[THREAD {robotname}] Waiting for input...")
        data = recv_wait(conn)
        if not data:
            continue

        if data in Protocol.move_command:
            buffer[robotname].append(data)
        elif regex_speed.match(data):
            speed_int = int(regex_speed.match(data).groups()[0])
            if not speed_int in range(0, 101):
                speed_int = 10
            speed_int = min(speed_int, ROBOT_DEFAULT_MAX_SPEED)
            buffer[robotname].append(f"{Protocol.speed} {speed_int}")
        else:
            print(f"[THREAD {robotname}] Command not understood : {data}")


def recv_wait(conn):
    while True:
        data = decode_byte_to_str(conn.recv(IN_BYTE_MAX_SIZE))
        if not data:
            time.sleep(ROBOT_BUFFER_REFRESH_TIME)
        else:
            return data


print("=================================")
print("=     ServerMonke Web Server    =")
print("=  Copyright© ReturnToMonke inc =")
print("=  2021                         =")
print("=================================\n")

print(f"Listening to port {PORT} for connections...\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()

        print(f"[MAIN] Received connection from {conn} {addr}")
        thread = threading.Thread(target=process_input, args=(conn, addr))
        thread.start()
        
