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
    #deixa o server aguardando coneção
    connectionSocket, addr = serverSocket.accept() #Recebe no connectionSocket os dados de endeço do outro socket e para onde envia-los e o que salvar os valores 
    #Recebo a stream e decodifico
    sentence = connectionSocket.recv(1024).decode()
    #Recebe novo endereço
    clientData = sentence.split('|')
    print("",clientData)
    #Passa pra maiscula
    capitalizedSentence = sentence.upper()
    #envia de volta os dados pro client
    connectionSocket.send(capitalizedSentence.encode())
    #Fecho a conecçao
    connectionSocket.close()