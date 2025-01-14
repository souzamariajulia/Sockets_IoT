import socket
import threading
import time

def handle_sensor(conn):
    porta_aberta_inicio = None  # Para monitorar o tempo de porta aberta

    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Recebido do sensor: {data}")

            
            sensor_id, valor = data.split(',')
            sensor_id = int(sensor_id)
            valor = valor.strip()

            if sensor_id == 1:  # Sensor de Temperatura
                temperatura = float(valor)
                print(f"Temperatura detectada: {temperatura}°C")
                if temperatura > 10.0: 
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as atuador_socket:
                        atuador_socket.connect(('127.0.0.1', 5001))
                        atuador_socket.sendall("LIGAR_REFRIGERACAO".encode('utf-8'))

            elif sensor_id == 2:  # Sensor de Porta
                porta_aberta = valor == "True"
                if porta_aberta:
                    if not porta_aberta_inicio:
                        porta_aberta_inicio = time.time()
                    elif time.time() - porta_aberta_inicio > 30:
                        print("Alarme: Porta aberta por mais de 30 segundos!")
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as atuador_socket:
                            atuador_socket.connect(('127.0.0.1', 5001))
                            atuador_socket.sendall("ALARME".encode('utf-8'))
                else:
                    porta_aberta_inicio = None 

        except Exception as e:
            print(f"Erro ao processar dados do sensor: {e}")
            break


def main():
    host, port = '127.0.0.1', 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Gerenciador aguardando conexões...")
        while True:
            conn, addr = s.accept()
            print(f"Conexão estabelecida com {addr}")
            threading.Thread(target=handle_sensor, args=(conn,)).start()

if __name__ == "__main__":
    main()
