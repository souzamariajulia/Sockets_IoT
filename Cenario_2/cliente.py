import socket
import time
import pygame

class SensorPorta:
    def __init__(self, id_sensor):
        self.id_sensor = id_sensor
        self.status = "Fechada"
        self.tempo_aberto = 0

    def abrir_porta(self):
        self.status = "Aberta"
        self.tempo_aberto = time.time() 

    def fechar_porta(self):
        self.status = "Fechada"
        self.tempo_aberto = 0

    def tempo_abrindo(self):
        """Retorna o tempo que a porta ficou aberta até agora."""
        if self.status == "Aberta":
            return time.time() - self.tempo_aberto
        return 0
    
def tocar_alarme():
    pygame.mixer.music.load("alarme.mp3")
    pygame.mixer.music.play()

def conectar_ao_servidor():
    sensor_porta = SensorPorta(id_sensor="SensorPorta1")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    while True:
        if sensor_porta.status == "Fechada":
            sensor_porta.abrir_porta()
            print("Porta aberta.")
        
        if sensor_porta.status == "Aberta" and sensor_porta.tempo_abrindo() >= 30:
            print("Alarme ativado! Porta aberta por mais de 30 segundos.")
            tocar_alarme()
        
        client_socket.send(f"PORTA:{sensor_porta.status}".encode('utf-8'))

        resposta = client_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {resposta}")

        time.sleep(10) 

    client_socket.close()

conectar_ao_servidor()
