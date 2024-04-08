from socket import *
#Defino a porta do servidor
serverPort = 12000
#Crio o mesmo padrão de conecção do client
serverSocket = socket(AF_INET,SOCK_STREAM)
#Vincula o servidor a porta que escolhi
serverSocket.bind(('',serverPort))
#Torna o socket passivo na coneção
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    #deixa o server aguardando coneção
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()