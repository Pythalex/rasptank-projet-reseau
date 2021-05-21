import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
def register_connect_robot(socket, robot) :
    socket.sendall(robot.encode())
    return socket.recv(1024).decode("utf-8") 

def connect_server_register(robot) : 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    response = register_connect_robot(client_socket, f"register {robot}")
    print("response: ", response)
    client_socket.close()
    # if response == "ok" :
    #     print("Robot has been registered")
    # elif response == "already_used" :
    #     print("Robot is already registed") 
    # else :
    #     print("unknown error")   
    # return client_socket
    return response

def connect_server_connect_robot(robot) :
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    response = register_connect_robot(client_socket, f"connect {robot}")
    client_socket.close()

    # if response == "ok" :
    #     print("Connected to robot")
    # elif response == "already_used" :
    #     print("Robot is already connected to someone else") 
    # elif response == "unknown":
    #     print("Robot is unknown")
    # else :
    #     print("unknown error")
    # return client_socket
    print("here thee here thee: ", response)
    return response

print("Should be unknown : ", end="")
assert connect_server_connect_robot("swag") == "unknown"

print("Should be ok", end="")
assert connect_server_register("swag") == "ok"

print("Should be ok", end="")
assert connect_server_connect_robot("swag") == "ok"

print("Should be already_used", end="")
assert connect_server_connect_robot("swag") == "already_used"

print("Should be unknown", end="")
assert connect_server_connect_robot("hello") == "unknown"

print("Should be already_used", end="")
assert connect_server_register("swag") == "already_used"

print("===================")
print("= Everything is OK.")
print("===================")

#connect_server_register("swag")
#print('Received', repr(data))