import socket
import select
import sys


if len(sys.argv) < 2:
    print("usage: client SERVER_IP [PORT]")
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF INET indica que o endereço é internet
server.connect((ip_address, port))  # sockstrem, protocolo ip

running = True
while running:
    socket_list = [sys.stdin, server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es) 
    if ws:
        print("WRT:", ws) 
    for sock in rs: 
        if sock == server:
            message = sock.recv(2048).decode("utf-8") # recebe de volta do servidor
            print(message) # printa no terminal
        else:
            message = sys.stdin.readline() # Espera input do terminal
            server.send(message.encode("utf-8")) # Envia o input como texto para o server
            if message.upper() == "@SAIR\n": # Se a mensagem for @sair fecha o cliente
                sys.exit(1) # caso não haja o sysexit o cliente fica em um loop infinito sem resposta após ser desconectado do server

server.close()
