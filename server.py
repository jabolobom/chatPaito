import socket
import select
import sys
from threading import Thread

def chat_client(conn, addr): # precisaria rodar múltiplas instâncias dessa função para que o chat funcione?, monitorar vários
    # hosts ao mesmo tempo?
    client_connected = conn is not None

    try:
            while client_connected:
                server.listen(5)
                message = conn.recv(2048).decode("utf-8") # conn = socket / classe socket com métodos
                
                if message: # aqui provavelmente um if pra checar se a msg não é comando "@"
                    print(f"<{addr}>: {message}")
                    conn.send(f"<Voce: {addr}> {message}".encode("utf-8"))
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

running = True
while running:
    conn, addr = server.accept() # aceita a conexão, porém pausa o código until alguma conexão é aceita
    print(f"DEBUG: {addr} conectado")
    connectedUsers.append(conn)
    t1 = Thread(target=chat_client, args=(conn, addr))
    t1.start() # como comunicar todas as threads entre si?
    # var global?
        

server.close()
