#
# Auteur : ReturnToMonke inc
# Copyright 2021 tous droits réservés
# Reject Humanity tm
#

import socket
import threading
import sys
import time
from pynput.keyboard import Key, Listener


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
conn = None

IN_BYTE_MAX_SIZE = 1024
ROBOT_BUFFER_REFRESH_TIME = 10 / 1000 # 10 ms

class Protocol:
    forward = b"forward"
    backward = b"backward"
    left = b"left"
    right = b"right"
    speed = b"speed 100"
    move_command = [forward, backward, left, right]

    connect = "connect"

key_binding = {
    "up"    : Protocol.forward,
    "down"  : Protocol.backward,
    "left"  : Protocol.left,
    "right" : Protocol.right,
    "s"     : Protocol.speed
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


def on_press(key):
    try:
        conn.sendall(key_binding[key.name])
    except:
        try:
            conn.sendall(key_binding[key.char])
        except:
            pass

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def main():
    global conn

    print("=================================")
    print("=     CONTROLEUR ROBOTSWAG      =")
    print("=  Copyright© ReturnToMonke inc =")
    print("=  2021                         =")
    print("=================================")

    robotname = input("Enter robot name to connect to : ")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.sendall(f"{Protocol.connect} {robotname}".encode())
    data = conn.recv(IN_BYTE_MAX_SIZE).decode("utf-8")
    print(f"Server response : {data}")

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
main()