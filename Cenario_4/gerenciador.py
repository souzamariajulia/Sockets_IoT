import socket
import threading

# Classe para o Atuador de Luz Interna
class AtuadorLuzInterna:
    def __init__(self, id_atuador):
        self.id_atuador = id_atuador
        self.status = 'Desligado'

    def ligar(self):
        self.status = 'Ligado'
        print("Luz interna acesa.")

    def desligar(self):
        self.status = 'Desligado'
        print("Luz interna apagada.")


# Classe para o Sensor de Porta
class SensorPorta:
    def __init__(self, id_sensor):
        self.id_sensor = id_sensor
        self.status = "Fechada"

    def abrir_porta(self):
        self.status = "Aberta"

    def fechar_porta(self):
        self.status = "Fechada"


# Classe para o Gerenciador (Servidor)
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

                if data.startswith("PORTA"):
                    status_porta = data.split(":")[1]
                    print(f"Status da porta: {status_porta}")

                    if status_porta == "Aberta":
                        self.atuadores["LuzInterna"].ligar()  # Liga a luz interna
                    else:
                        self.atuadores["LuzInterna"].desligar()  # Desliga a luz interna

            except Exception as e:
                print(f"Erro: {e}")
                break

        client_socket.close()

    def iniciar(self):
        self.aceitar_conexao()


# Inicia o servidor (Gerenciador)
gerenciador = Gerenciador()

# Adiciona o Sensor de Porta e o Atuador de Luz Interna
sensor_porta = SensorPorta(id_sensor="SensorPorta1")
gerenciador.adicionar_sensor(sensor_porta)

atuador_luz = AtuadorLuzInterna(id_atuador="LuzInterna")
gerenciador.adicionar_atuador(atuador_luz)

gerenciador.iniciar()
