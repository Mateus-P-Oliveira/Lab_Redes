import socket
import threading
import queue
import os

messages = queue.Queue()
clients = []
aliases = []
#Recebe o Socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1",9999))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message,addr)) #Coloca as mensagens na fila 
        except:
            pass

def broadcast():
    while True:
        while not messages.empty(): #Enquanto nao esvaziar a fila 
            message, addr = messages.get() 
            print(message.decode())            
            segmentMessage = message.decode('utf-8')
            if "/" in segmentMessage:
                segmentMessage = segmentMessage.split("/")
                #print("____________")
                print(segmentMessage)  # print the whole list
                #print("Adasdsd")
                print(segmentMessage[1]) 
            else:
                print("No '/' in the message")
            
            if addr not in clients: #Caso o endereço nao exista adiciona o usuario no servidor 
                clients.append(addr)
                
                segmentMessage = segmentMessage.split(":")
                
                aliases.append(segmentMessage[1])
                
            if segmentMessage[1] == "send":  #Mudar aqui pq a mensagem inclui o nome do usuario no padrão nome: /send 
                target = segmentMessage[2]
                #print("Ola")
                #print(target)
                #print("________________________")
                #print(aliases)
                if target in aliases:
                    #print("errrrr")
                    targetIndex = aliases.index(target)
                    server.sendto(message, clients[targetIndex])
            elif segmentMessage[1].startswith("file"): #Se a mensagem começa com /file
                if(segmentMessage[2] == "all"):
                    
                    filename = segmentMessage[3]#[1]
                    #content = '\\n'.join(segmentMessage[2].split('\\n')[1:])
                    #with open(filename, 'w') as f:
                        #f.write(content)
                    print(f"Received file {filename}")
                    message = f"/file/{filename}"
                    #print("*********************")
                    for client in clients: #Percorre a lista de clientes para enviar a mensagem
                        #print("*********************")
                        try:                            
                                #print("OSOSOSOSOSOSOOSOSO")
                                print(message)                     
                                server.sendto(message.encode(),client)
                        except:
                                clients.remove(client)
                if(segmentMessage[2] == "send"):  
                    filename = segmentMessage[4]#[1]
                    #content = '\\n'.join(segmentMessage[2].split('\\n')[1:])
                    #with open(filename, 'w') as f:
                        #f.write(content)
                    print(f"Received file {filename}")
                    message = f"/file/{filename}"
                    target = segmentMessage[3]
                    if target in aliases:
                        #print("errrrr")
                        targetIndex = aliases.index(target)
                        server.sendto(message.encode(), clients[targetIndex])
                                
                
            else: #Caso não envia para todo mundo
                for client in clients: #Percorre a lista de clientes para enviar a mensagem
                    try:
                        if message.decode().startswith("SIGNUP_TAG:"): #Se começa com SIGNUP_TAG a mensagem de usuario joined é enviada
                            name = message.decode()[message.decode().index(":")+1:]
                            server.sendto(f"{name} joined!".encode(), client)
                        else:                      
                            server.sendto(message,client)
                    except:
                        clients.remove(client)
                    
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)  

t1.start()
t2.start()