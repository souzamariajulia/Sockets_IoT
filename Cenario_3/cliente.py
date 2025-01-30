import socket

def consultar_estoque():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    client_socket.send("CONSULTA_ESTOQUE".encode('utf-8'))

    resposta = client_socket.recv(1024).decode('utf-8')
    print(f"Resposta do servidor: {resposta}")

    client_socket.close()

consultar_estoque()
