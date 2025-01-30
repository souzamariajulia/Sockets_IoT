import socket
import threading
import random
import time

class AtuadorRefrigerador:
    def __init__(self, id_atuador):
        self.id_atuador = id_atuador
        self.status = 'Desligado'

    def ligar(self):
        self.status = 'Ligado'
        print("Refrigerador ligado para reduzir a temperatura.")

    def desligar(self):
        self.status = 'Desligado'
        print("Refrigerador desligado. Temperatura ideal atingida.")

class Gerenciador:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.atuadores = {}
        self.temperatura_limite = 5
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Gerenciador (Servidor) ouvindo na porta {self.port}...")

    def adicionar_atuador(self, atuador):
        self.atuadores[atuador.id_atuador] = atuador

    def aceitar_conexao(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Nova conexão de {client_address}")
            threading.Thread(target=self.tratar_cliente, args=(client_socket,)).start()

    def tratar_cliente(self, client_socket):
        repeticoes = 0 
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                if data.startswith("TEMP"):
                    temperatura_atual = float(data.split(":")[1])
                    print(f"Temperatura atual recebida: {temperatura_atual}°C")

                    if temperatura_atual >= self.temperatura_limite:
                        self.atuadores["Refrigerador"].ligar()
                        self.simular_ajuste_temperatura(client_socket)
                    else:
                        self.atuadores["Refrigerador"].desligar()
                        client_socket.send("Temperatura ideal atingida.".encode('utf-8'))

                repeticoes += 1
                if repeticoes >= 5:
                    print("Encerrando a conexão.")
                    break

            except Exception as e:
                print(f"Erro: {e}")
                break

        client_socket.close()

    def simular_ajuste_temperatura(self, client_socket):
        for _ in range(3):
            time.sleep(1)
            nova_temperatura = random.uniform(self.temperatura_limite - 2, self.temperatura_limite)
            print(f"Temperatura ajustando para: {nova_temperatura:.2f}°C")
            if nova_temperatura <= self.temperatura_limite:
                break
        client_socket.send("Temperatura ajustada para o limite ideal.".encode('utf-8'))

    def iniciar(self):
        self.aceitar_conexao()

gerenciador = Gerenciador()
gerenciador.adicionar_atuador(AtuadorRefrigerador("Refrigerador"))
gerenciador.iniciar()
