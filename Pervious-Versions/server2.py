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
    #while connected:
    account_length=conn.recv(HEADER).decode(FORMAT)
    print(account_length)
    #if account_length:
    account_length=int(float(account_length))
    print(account_length) 
    account=conn.recv(account_length).decode(FORMAT)
    password_length=conn.recv(HEADER).decode(FORMAT)
    password_length=int(float(password_length))
    print(password_length)
    password=conn.recv(password_length).decode(FORMAT)
    #if account==DISCONNECT_MESSAGE:
    #connected=False
    try:
        f=open(account+'.txt','r')
        line=f.readline()
        l=line.split()
        account=l[0]
        acc_pass=l[1]
        balance=l[2]
        if(acc_pass!=password):
            conn.send("Incorrect Password! Please try again".encode(FORMAT))
            password=conn.recv(HEADER).decode(FORMAT)
            if(acc_pass!=password):
                exit
        else:
            conn.send("Openened Successfully".encode(FORMAT))
        print(line)

    except:
        conn.send("Account did not exist. Creating new account".encode(FORMAT))
        f=open(account+'.txt','w')
        balance_length=conn.recv(HEADER).decode(FORMAT)
        balance=int(float(balance_length))
        balance=conn.recv(HEADER).decode(FORMAT)
        f.write(account+" "+password+" "+balance)
    f.close()
    f=open(account+'.txt','r+')
    conn.send("Enter 1: check balance 2:transfer fund 3:change password 4:Exit".encode(FORMAT))
    option_length=conn.recv(HEADER).decode(FORMAT)
    print(option_length)
    option_length=int(float(option_length))
    option=conn.recv(option_length).decode(FORMAT)
    option=int(float(option))
    print(option)
    while(option<=4):
        if(option==1):
            conn.send(f"Your balance is {balance}".encode(FORMAT))
        elif(option==2):
            conn.send("Enter amount to transfer".encode(FORMAT))
            amt_length=conn.recv(HEADER).decode(FORMAT)
            amt_length=int(float(amt_length))
            amt=conn.recv(amt_length).decode(FORMAT)
            amt=int(float(amt))
            balance=int(balance)
            if(amt<balance):
                balance=balance-amt
                balance=str(balance)
                f.write(account+" "+password+" "+balance)
                conn.send("Transfer was successfull!".encode(FORMAT))
            else:
                conn.send("Transferable Amount was more than balance, please try again".encode(FORMAT))
        elif(option==3):
            conn.send("Enter new password".encode(FORMAT))
            password_length=conn.recv(HEADER).decode(FORMAT)
            password_length=int(float(password_length))
            password=conn.recv(password_length).decode(FORMAT)
            f.write(account+" "+password+" "+balance)
        elif(option==4):
            conn.send("EXIT".encode(FORMAT))
            conn.close()
            exit(1)
        conn.send("Enter 1: check balance 2:transfer fund 3:change password 4:Exit".encode(FORMAT))
        option_length=conn.recv(HEADER).decode(FORMAT)
        print(option_length)
        option_length=int(float(option_length))
        option=conn.recv(option_length).decode(FORMAT)
        option=int(float(option))
        print(option)
            





    # with open(account+'.txt','w') as f:
    #     f.write(account+" "+password)


    print(f"{account} {password}")
            #print(f"[{addr}] {msg}")
            #x=input()
            #conn.send(x.encode(FORMAT))

            
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTINING] Server is listening on {SERVER}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() -1} .")


print("Server is starting ...")
start()