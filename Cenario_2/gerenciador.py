import socket
import threading
import time

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


class Gerenciador:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.porta_aberta_tempo = 0  
        self.atuadores = {}
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
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                if data.startswith("PORTA"):
                    status_porta = data.split(":")[1]
                    print(f"Status da porta: {status_porta}")

                    if status_porta == "Aberta":
                        self.porta_aberta_tempo += 1
                        if self.porta_aberta_tempo >= 30:
                            if self.atuadores["Alarme"].status == 'Desligado':  
                                self.atuadores["Alarme"].ligar()
                                client_socket.send("Alerta: Porta aberta por mais de 30 segundos.".encode('utf-8'))
                    else:
                        self.porta_aberta_tempo = 0
                        self.atuadores["Alarme"].desligar() 

            except Exception as e:
                print(f"Erro: {e}")
                break

        client_socket.close()

    def iniciar(self):
        self.aceitar_conexao()

gerenciador = Gerenciador()
gerenciador.adicionar_atuador(AtuadorAlarme("Alarme"))
gerenciador.iniciar()
