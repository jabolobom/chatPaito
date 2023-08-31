import socket
import select
import sys
from threading import Thread
from queue import Queue

fila = list()
read = list()

def chat_printer(conn, addr, proxMsg): # precisaria rodar múltiplas instâncias dessa função para que o chat funcione?, monitorar vários
    # hosts ao mesmo tempo?
    
    for x in proxMsg:
        if x not in read:
            print(f"<{addr}: {x}")
            conn.send(f"<{addr}> {x}".encode("utf-8"))
            read.append(x)
        else: continue
    

def chat_listener(conn, addr):
    client_connected = conn is not None
    global fila

    try:
        while client_connected:
            message = conn.recv(2048).decode("utf-8") # conn = socket / classe socket com métodos
            if message:    
                fila.append(message)
                chat_printer(conn, addr, proxMsg=fila)
            else:
                client_connected = False
                print(f"DEBUG: {addr} desconectado.")                
    except Exception as ex:
        print("ERROR: ", ex)

    conn.close()
     

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define o que é server
port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000 # define a porta

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port)) # liga o socket a um endereço específico,
server.listen(5) # espera pra entrar

running = True
while running:
    conn, addr = server.accept() # aceita a conexão, porém pausa o código until alguma conexão é aceita
    print(f"DEBUG: {addr} conectado")
    # connectedUsers = []
    # connectedUsers.append(conn)
    t1 = Thread(target=chat_listener, args=(conn, addr))
    t1.start() # como comunicar todas as threads entre si?
    # var global?
        

server.close()
