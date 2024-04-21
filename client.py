import threading
import socket
import os

alias = input("Choose an alias >>> ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 59000))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "alias?":
                client.send(alias.encode("utf-8"))
            elif message.startswith("/file"):
                print("OOooooOOOO")
                filename = message.split()[3]
                content = message.split("\\n", 1)[3]
                with open(filename, 'w') as f:
                    f.write(content)
                print(f"Received file {filename}")
            else:
                print(message)
        except:
            print("Error!")
            client.close()
            break

def client_send():
    while True:
        message = input("")
        if message.startswith("/file"):
            filename = message.split("/")[3] #Adaptar aqui para os padrões de envio que estou usando 
            print("OoooooooO")
            print(filename)
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    lines = f.read()
                    print(lines)
                message = f"{alias}: {message}\n{lines}"
        else:
            message = f'{alias}: {message}'
        client.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
