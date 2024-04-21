import socket
import threading
import random
import os

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            if message.decode().startswith("/file"):
                #print("*******************")
                filename = message.decode().split('/')
                
                filename = filename[2].split("\\n")
                #print(filename)
                content = '\\n'.join(message.decode().split('\\n')[1:])
                content = content + "\n" #Teste se atualiza o documento
                #print(content)                
                with open(filename[0], 'w') as f:
                    f.write(content)
                print(f"Received file {filename}")
            else:
                print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(),("127.0.0.1",9999)) #Isso cadastra o usuario no servidor

while True:
    message = input("")
    if message == "!q":
        exit()
    elif message.startswith("/file"):
        filename = message.split('/')[3]
        #print(filename)
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                lines = f.read()
            message = f"/file/{message.split('/')[2]}/{filename}\\n{lines}"
        #print(message)    
        client.sendto(f"{name}: {message}".encode(), ("127.0.0.1",9999))
    else:
        #print(message)
        client.sendto(f"{name}: {message}".encode(), ("127.0.0.1",9999))
