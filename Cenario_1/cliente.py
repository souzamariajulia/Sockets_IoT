import socket
import time

# Sensor de temperatura
class SensorTemperatura:
    def __init__(self, id_sensor, temperatura_inicial):
        self.id_sensor = id_sensor
        self.temperatura = temperatura_inicial

    def ler_temperatura(self):
        return self.temperatura


# Função que conecta o cliente ao servidor 
def conectar_ao_servidor():
    sensor = SensorTemperatura(id_sensor="SensorTemp1", temperatura_inicial=8.0)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    while True:
        temperatura = sensor.ler_temperatura()
        print(f"Enviando temperatura: {temperatura}°C")
        client_socket.send(f"TEMP:{temperatura}".encode('utf-8'))
        
        # espera a resposta
        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}")

        # 
        time.sleep(10)  #envia leitura a cada 10 segundos 
        sensor.temperatura += 0.5 

    client_socket.close()


# inicia o cliente 
conectar_ao_servidor()
