from asyncio.base_events import Server
import socket
import threading

HEADER=64
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())  #to get host ip address
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    server.send(send_length)
    server.send(message)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(float(msg_length)) 
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MESSAGE:
                connected=False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTINING] Server is listening on {SERVER}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() -1} .")

print("Server is starting ....")
start()