import socket
import time

class SensorPorta:
    def __init__(self, id_sensor):
        self.id_sensor = id_sensor
        self.status = "Fechada"

    def abrir_porta(self):
        self.status = "Aberta"

    def fechar_porta(self):
        self.status = "Fechada"


def conectar_ao_servidor():
    sensor_porta = SensorPorta(id_sensor="SensorPorta1")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    while True:
        if sensor_porta.status == "Fechada":
            sensor_porta.abrir_porta()
            print("Porta aberta.")
        else:
            sensor_porta.fechar_porta()
            print("Porta fechada.")
        
        client_socket.send(f"PORTA:{sensor_porta.status}".encode('utf-8'))

        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}")

        time.sleep(10) 

    client_socket.close()
    
conectar_ao_servidor()
