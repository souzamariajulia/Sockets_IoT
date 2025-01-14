import socket
import time

#Cenário 1
def Temperatura():
    sensor_id = 1
    host, port = '127.0.0.1', 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            temperatura = 8.0
            mensagem = f"{sensor_id},{temperatura}"
            s.sendall(mensagem.encode('utf-8'))
            print(f"Sensor enviou: {mensagem}")
            time.sleep(10)

if __name__ == "__main__":
    Temperatura()

#Cenário 2 
def PortaAberta():
    sensor_id = 2
    host, port = '127.0.0.1', 5001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            porta_aberta = True
            mensagem = f"{sensor_id}, {porta_aberta}"
            s.sendall(mensagem.encode('utf-8'))
            print(f"Sensor de porta enviou: {mensagem}")
            time.sleep(5) #envia atualização a cada 5 segundos 

if __name__ == "__main__":
    PortaAberta()

#Cenário 3
