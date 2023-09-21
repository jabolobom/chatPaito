import socket
import select
import sys
from threading import Thread
from datetime import datetime

time = datetime.now().strftime("%H:%M:%S") # Guarda o tempo atual, salva junto com as mensagens na respectiva lista
print("Server aberto as:", time) # Mensagem de startup

def chat_client(conn, addr): # Função principal, aceita e envia mensagens, organiza apelidos e ultimas mensagens.
    client_connected = conn is not None # Permite o loop infinito

    try: # Identação estranha, tentei arrumar e alguma coisa quebrou, decidi deixar assim;
            
            conn.send("Insira seu apelido".encode("utf-8"))
            apelido = conn.recv(2048).decode("utf-8")
            apelido = apelido[:-1]
            conn.send(f"Bem-vindo, {apelido}".encode("utf-8"))
            

            while client_connected: 
                message = conn.recv(2048).decode("utf-8") # Loop infinito que espera uma mensagem do cliente 
                
                if message: # Tratamento da mensagem
                    print(f"<{addr}>: {message}") # Print no server
                    conn.send(f"{apelido} ({addr[1]}):: {message}".encode("utf-8")) # Reenvia "formatada" pro cliente

                    if message.upper() == "@SAIR\n": # Checagem de comando
                        client_connected = False
                        connectedUsers.remove(conn) # Remove da lista pra evitar erros no repasse de mensagens
                        conn.send("DESCONECTAR".encode("utf-8"))
                        print(f"DEBUG: {addr} se desconectou!")
                    elif message.upper() == "@ORDENAR\n": # Checagem de outro comando
                        for elemento in msgList: # Mostra as últimas 15 mensagens na seguinte ordem: Tempo, Apelido(Porta), Mensagem
                            conn.send(f"({elemento[2]}), {elemento[0]} ({elemento[1]}) disse:: {elemento[3]}".encode("utf-8"))
                        
                    if len(msgList) > 15: # Caso ja existam 15 mensagens, remove a mais antiga
                        msgList.pop(0) 
                        msgList.append([apelido, addr[1], time, message])
                    else: # Coloca toda mensagem recebida em uma lista, junto com o horário recebido + nome e porta do usuário
                        msgList.append([apelido, addr[1], time, message]) 

                    for user in connectedUsers: # Repassa a mensagem formatada para os outros usuários conectados
                         if user != conn:
                            try:
                              user.send(f"<{apelido}({addr[1]}) :: {message}".encode("utf-8"))
                            except: # Caso falhe em repassar, remove o usuário dos conectados
                                connectedUsers.remove(user)
                                user.close()

                else: # Caso receba qualquer coisa que não seja uma mensagem, desconecta e remove o user da lista de ativos
                    client_connected = False
                    connectedUsers.remove(conn)
                    print(f"DEBUG: {addr} desconectado.")

    except Exception as ex:
        print("ERROR: ", ex)
    conn.close() # Fecha a porta
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define o que é server
port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000 # define a porta


server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port)) # Liga o socket a um endereço específico
server.listen(5) # Espera requisições de conexão

connectedUsers = list()
msgList = list() # Lista de usuários conectados e últimas mensagens

running = True
while running:
    conn, addr = server.accept() # Quando requerido, aceita o pedido de conexão
    print(f"DEBUG: {addr} conectado")
    connectedUsers.append(conn) # Coloca o endereço do usuário n lista de conectados
    
    t1 = Thread(target=chat_client, args=(conn, addr)) # Cria uma thread com a função principal
    t1.start() # Após aceitar uma conexão, inicia uma thread com a funao chat_client

server.close() # Fecha o server caso o loop termine (não acontece)
