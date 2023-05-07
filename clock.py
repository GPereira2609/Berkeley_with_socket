import socket
import time

from datetime import datetime
from random import randint

HOST = 'localhost'
PORT = 5000

def get_time():
    # retorna o tempo atual em segundos
    return time.time() + randint(1000, 3000)

def main():
    # cria o socket do cliente e se conecta ao servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    # envia o tempo atual para o servidor
    t = get_time()

    print(f"A hora atual do relógio é: {datetime.fromtimestamp(t).time().isoformat('seconds')}")

    time.sleep(2)

    print("Enviando hora para o Daemon")
    client_socket.sendall(str(t).encode())

    data = client_socket.recv(1024)
    new_time = float(data.decode())

    t = new_time

    time.sleep(2)
    print(f"Tempo ajustado: {datetime.fromtimestamp(t).time().isoformat('seconds')}")

    client_socket.close()

if __name__ == '__main__':
    main()
