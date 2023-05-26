from distutils.command.clean import clean
from inspect import classify_class_attrs
from random import choice
import socket


HEADER=64
PORT=5050
FORMAT='utf-8'
DISCONNECT_MESSAGE="!DISCONNECT"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    #print(client.recv(2048).decode(FORMAT))

x=input("Enter Bank Account Name: ")
send(x)
y=input("Enter Password: ")
send(y)
a=client.recv(HEADER).decode(FORMAT)
#print(a+"tryyy")
#a1=int(a1)
#a2=client.recv(a1).decode(FORMAT)
if(a=="Account did not exist. Creating new account"):
    print(a)
    balance=input("Enter amount to be deposited: ")
    send(balance)
elif(a=="Incorrect Password! Please try again"):
    password=input("Incorrect Password! Please try again: ")
    send(password)
elif(a=="Openened Successfully"):
    print(a)
b=client.recv(HEADER).decode(FORMAT)
if(b=="Enter 1: check balance 2:transfer fund 3:change password 4:Exit"):
    print("\n")
    while(b!="EXIT"):
        choice=input("Enter 1: check balance 2:transfer fund 3:change password 4:Exit: ")
        send(choice)
        c=client.recv(HEADER).decode(FORMAT)
        if("Your balance is" in c):
            print(c)
        elif(c=="Enter amount to transfer"):
            d=input("Enter amount to transfer: ")
            send(d)
            f=client.recv(HEADER).decode(FORMAT)
            print(f)
        elif(c=="Enter new password"):
            e=input("Enter new password: ")
            send(e)
        elif(c=="EXIT"):
            print(c)
            exit(1)
        b=client.recv(HEADER).decode(FORMAT)


send(DISCONNECT_MESSAGE)

