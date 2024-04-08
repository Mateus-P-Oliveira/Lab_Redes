from socket import *
serverName = '0.0.0.0' # mudar depois Caso necessario 
serverPort = 12000
#Escolho tipo de conecçao como tendo so ip e porta e conexão bidirecional entre cliente e servidor
clientSocket = socket(AF_INET, SOCK_STREAM)
#Coloco o nome do servidor e a porta 
clientSocket.connect((serverName,serverPort))
#Insert the message 
sentence = input('Input lowercase sentence:')
#Envio a setença
clientSocket.send(sentence.encode())
#Recebo a stream
modifiedSentence = clientSocket.recv(1024)
#dou print no que recebi 
print ('From Server:', modifiedSentence.decode())
#Feço a conecção
clientSocket.close()