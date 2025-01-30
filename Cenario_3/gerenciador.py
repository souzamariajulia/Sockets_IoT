import socket
import threading

class AtuadorAlarme:
    def __init__(self, id_atuador):
        self.id_atuador = id_atuador
        self.status = 'Desligado'

    def ligar(self):
        self.status = 'Ligado'
        print("ALERTA: Porta aberta por mais de 30 segundos!")

    def desligar(self):
        self.status = 'Desligado'
        print("Alarme desligado.")

class SensorEstoque:
    def __init__(self, id_sensor, nivel_estoque_inicial):
        self.id_sensor = id_sensor
        self.nivel_estoque = nivel_estoque_inicial 

    def ler_nivel_estoque(self):
        return self.nivel_estoque

class Gerenciador:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.sensores = {}
        self.atuadores = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Gerenciador (Servidor) ouvindo na porta {self.port}...")

    def adicionar_atuador(self, atuador):
        self.atuadores[atuador.id_atuador] = atuador

    def adicionar_sensor(self, sensor):
        self.sensores[sensor.id_sensor] = sensor

    def aceitar_conexao(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Nova conexão de {client_address}")
            threading.Thread(target=self.tratar_cliente, args=(client_socket,)).start()

    def tratar_cliente(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                if data.startswith("CONSULTA_ESTOQUE"):
                    sensor = self.sensores.get("SensorEstoque1")
                    if sensor:
                        nivel_estoque = sensor.ler_nivel_estoque()
                        resposta = f"Estoque atual: {nivel_estoque}%"
                        client_socket.send(resposta.encode('utf-8'))

            except Exception as e:
                print(f"Erro: {e}")
                break

        client_socket.close()

    def iniciar(self):
        self.aceitar_conexao()

gerenciador = Gerenciador()
sensor_estoque = SensorEstoque(id_sensor="SensorEstoque1", nivel_estoque_inicial=30)
gerenciador.adicionar_sensor(sensor_estoque)

gerenciador.iniciar()
