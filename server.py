import socket
import select
import sys
from threading import Thread
from datetime import datetime

time = datetime.now().strftime("%H:%M:%S")
print("Server aberto as:", time)


def chat_client(conn, addr):
    client_connected = conn is not None

    try:
            while client_connected:
                
                message = conn.recv(2048).decode("utf-8") 
                
                if message: 
                    print(f"<{addr}>: {message}")
                    conn.send(f"<Voce:> {message}".encode("utf-8"))

                    if message.upper() == "@SAIR\n":
                        client_connected = False
                        connectedUsers.remove(conn)
                        conn.send("DESCONECTAR".encode("utf-8"))
                        print(f"DEBUG: {addr} se desconectou!")

                    if len(msgList) > 15:
                        msgList.pop(0)
                        msgList.append([addr[1], time, message])
                    else:
                        msgList.append([addr[1], time, message])


                    for user in connectedUsers:
                         if user != conn:
                            try:
                              user.send(f"<User: {addr}> says: {message}".encode("utf-8"))
                            except:
                                connectedUsers.remove(user)
                                user.close()
                else:
                    client_connected = False
                    connectedUsers.remove(conn)
                    print(f"DEBUG: {addr} desconectado.")

    except Exception as ex:
        print("ERROR: ", ex)
    conn.close()
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define o que é server
port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000 # define a porta


server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port)) # liga o socket a um endereço específico,
server.listen(5) # espera pra entrar

connectedUsers = list()
msgList = list()

running = True
while running:
    conn, addr = server.accept() # aceita a conexão, porém pausa o código until alguma conexão é aceita
    print(f"DEBUG: {addr} conectado")
    connectedUsers.append(conn)
    t1 = Thread(target=chat_client, args=(conn, addr))
    t1.start() # como comunicar todas as threads entre si?
    # var global?
        

server.close()
