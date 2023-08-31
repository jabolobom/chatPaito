import socket
import select
import sys
from threading import Condition

from server import fila

condicao = Condition()

def msgTemp():
    condicao.acquire()


def chat_printer(conn, addr, proxMsg): # precisaria rodar múltiplas instâncias dessa função para que o chat funcione?, monitorar vários
    # hosts ao mesmo tempo?

    read = list()
    for x in proxMsg:
        if x not in read:
            print(f"<{addr}: {x}>")
            conn.send(f"<{addr}> {x}")
            read.append(x)
            break
        else: continue

    # if message: # aqui provavelmente um if pra checar se a msg não é comando "@"
    #     print(f"<{addr}>: {message}")
    #     conn.send(f"<{addr}> {message}".encode("utf-8"))
    #     # for user in connectedUsers: conn.send(f"{addr}{message}".enconde("utf-8"))
    #     # nao funciona
    # else:
    #     client_connected = False
    #     print(f"DEBUG: {addr} desconectado.")

def chat_listener(conn, addr):
    client_connected = conn is not None
    fila = list()

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
     