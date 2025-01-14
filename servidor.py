import socket 
import threading

def handle_sensor(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if data:
            print(f"Recebido do sensor: {data}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as atuador_socket:
                atuador_socket.connect(('127.0.0.1', 5001))
                atuador_socket.sendall("LIGAR".encode('utf-8'))


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