import socket

def main():
    host, port = '127.0.0.1', 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        consulta = "CONSULTA_ESTADO"
        s.sendall(consulta.encode('utf-8'))
        resposta = s.recv(1024).decode('utf-8')
        print(f"Cliente recebeu: {resposta}")

if __name__ == "__main__":
    main()