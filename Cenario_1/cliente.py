import socket
import time

class SensorTemperatura:
    def __init__(self, id_sensor, temperatura_inicial):
        self.id_sensor = id_sensor
        self.temperatura = temperatura_inicial

    def ler_temperatura(self):
        return self.temperatura


def conectar_ao_servidor():
    sensor = SensorTemperatura(id_sensor="SensorTemp1", temperatura_inicial=8.0)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    while True:
        temperatura = sensor.ler_temperatura()
        print(f"Enviando temperatura: {temperatura}°C")
        client_socket.send(f"TEMP:{temperatura}".encode('utf-8'))
        
        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}")

        # 
        time.sleep(10) 
        sensor.temperatura += 0.5 

    client_socket.close()

conectar_ao_servidor()
