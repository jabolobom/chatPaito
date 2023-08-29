import socket
import select
import sys


if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF INET indica que o address é internet
server.connect((ip_address, port))  # sockstrem é o protocolo ip
socket.socket().setblocking(False)

running = True
while running:
    socket_list = [sys.stdin, server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es) # errors
    if ws:
        print("WRT:", ws) # writers  ?
    for sock in rs: # readers?
        if sock == server:
            message = sock.recv(2048).decode("utf-8")
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message.encode("utf-8"))

server.close()
