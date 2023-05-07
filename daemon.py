
import time
import socket

from datetime import datetime
from threading import Thread
from random import randint

HOST = 'localhost'
PORT = 5000
max_workers = 2

relogios = []

hora_atual = time.time() + randint(1000, 3000)

def get_media():
    horas = []
    for relogio in relogios:
        data = relogio.recv(1024)
        horas.append(float(data))
    
    horas.append(float(hora_atual))

    media = sum(horas)/len(horas)

    return media

def broadcast(avg):
    hora_atual = avg
    for relogio in relogios:
        msg = str(f"{avg}").encode()
        relogio.sendall(msg)
    time.sleep(2)
    print(f"Relógios ajustados para: {datetime.fromtimestamp(hora_atual).time().isoformat('seconds')}")

def main():
    daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    daemon.bind((HOST, PORT))
    daemon.listen()
    print(f"""
    Ouvindo...
    Host = {HOST}
    Porta = {PORT}
    """)

    time.sleep(2)

    print(f"A hora atual do Daemon é: {datetime.fromtimestamp(hora_atual).time().isoformat('seconds')}")

    while True:
        clock, ender = daemon.accept()
        relogios.append(clock)
        print(f"Conexão estabelecida com relógio {ender}")

        if len(relogios) == max_workers:
            media = get_media()
            broadcast(media)
            break

if __name__ == "__main__":
    main()