import threading
import socket
import os

host = "127.0.0.1"
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []

def broadcast(message):
    for client in clients:       
        client.send(message)

def privateMessage(message,clientTarget):    
    for y in range(len(aliases)):   
        aliasSt = str(aliases[y])
        aliasesStrip = aliasSt.strip()
        clientTargetStrip = clientTarget.strip()
        if aliasesStrip == clientTargetStrip:         
            x= 0
            for client in clients: 
                if x == y:  
                    client.send(message)
                x+= 1

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            segmentMessage = message.decode('utf-8')
            print(segmentMessage)
            segmentMessage = segmentMessage.split("/")
            print("shhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            print(segmentMessage[1])
            if(segmentMessage[1] == "send"):              
               privateMessage(message,segmentMessage[2])               
            if(segmentMessage[1] == "all"):  
                broadcast(message)
            if(segmentMessage[1] == "file"):
                print("sjdfnsdjfhdjf")
                if(segmentMessage[2] == "send"):
                    filename = segmentMessage[3]
                    if os.path.isfile(filename):
                        with open(filename, 'r') as f:
                            lines = f.read()
                        message = f"{segmentMessage[0]}: /file {filename}\n{lines}".encode('utf-8')
                        privateMessage(message,segmentMessage[4])
                if(segmentMessage[2] == "all"):
                    print("IIOSIIS" )
                    filename = segmentMessage[3]
                    print(filename)
                    if os.path.isfile(filename):
                        with open(filename, 'r') as f:
                            lines = f.read()
                        print("sdsdsdsdsdsdsdsdsdadsdasdasda")    
                        message = f"{segmentMessage[0]}: /file {filename}\n{lines}".encode('utf-8')
                        print("88888888888888888888888888")
                        broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chat room!".encode("utf-8"))
            aliases.remove(alias)
            break

def receive():
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f"connection is established with {str(address)}")
        client.send("alias?".encode("utf-8"))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of this client is {alias}".encode("utf-8"))
        broadcast(f"{alias} has connected to the chat room".encode("utf-8"))
        client.send("you are now connected!".encode("utf-8"))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()