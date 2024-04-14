# TCP

import threading
import socket

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


#Isso ira procurar na lista de endereços o cliente com mesmo ID e ira mandar para ele a mensagem 
def privateMessage(clientTarget):    
    
    for y in range(len(aliases)):   
       # print(aliases[0])  
        print(y)   
        if aliases[y] == clientTarget:            
            for client in clients: 
                if x == y:  #Arrumar aqui
                    print(x)
                    print("~~~~~~~~~~")
                    print(y)      
                    client.send(message)
                else:
                    x+= 1
           
   

# Function to handle clients'connections



def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            # Segmenta a mensagem---------------------
            segmentMessage = message.decode('utf-8')
            segmentMessage = segmentMessage.split("/")
            print(segmentMessage[1])
            if(segmentMessage[1] ==  "send"):               
               privateMessage(segmentMessage[1])
            #--------------------------
            broadcast(message) #Aqui é feito o envio de broadcast
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chat room!".encode("utf-8"))
            aliases.remove(alias)
            break


# Main function to receive the clients connection


def receive():
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f"connection is established with {str(address)}")
        client.send("alias?".encode("utf-8"))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        #--Dicionario com alias e seu respectivo client
        
        
        #-------------------------------------------------
        print(f"The alias of this client is {alias}".encode("utf-8"))
        broadcast(f"{alias} has connected to the chat room".encode("utf-8"))
        client.send("you are now connected!".encode("utf-8"))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
