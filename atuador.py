#São os trabalhadores do sistema, fazem coisas como ligar o motor do refrigerador, ascender luz, tocar alarme...

import socket

def Temperatura():
    atuador_id = 1  # Refrigerador
    host, port = '127.0.0.1', 5001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            comando = s.recv(1024).decode('utf-8')
            if comando:
                print(f"Atuador recebeu comando: {comando}")

if __name__ == "__main__":
    Temperatura()

def Alarme():
    atuador_id = 2
    host, port = '127.0.0.1'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.listen()
        print("Atuador (Alarme) aguardando comandos")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexão estabelecida com {addr}")
                dado = conn.recv(1024).decode('utf-8')
                if dado == "ALARME":
                    print("Alarme: Emitindo alerta sonoro!")
                if not dado:
                    break
if __name__ == "__main__":
    Alarme()







