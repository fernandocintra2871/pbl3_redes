import socket
import threading
import json
import os
from time import sleep

"""
$env:host="127.0.0.1"; $env:port="12001"; $env:clock2_host="127.0.0.1"; $env:clock2_port="12002"; $env:clock3_host="127.0.0.1"; $env:clock3_port="12003"; ; python3 app.py 
$env:port="12001"; $env:clock2_port="12002"; $env:clock3_port="12003"; python3 app.py
$env:port="12002"; $env:clock2_port="12001"; $env:clock3_port="12003"; python3 app.py 
$env:port="12003"; $env:clock2_port="12002"; $env:clock3_port="12001"; python3 app.py 

"""

host = "127.0.0.1"
port = int(os.environ.get("port"))

clock2_host = "127.0.0.1"
clock2_port = int(os.environ.get("clock2_port"))

clock3_host ="127.0.0.1"
clock3_port = int(os.environ.get("clock3_port"))

time = 0
drift = 1
clocks = {}
entry_detection = False

def handle_client(client_socket, client_address):
    global time
    #print(f'Conexão estabelecida com {client_address}')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = json.loads(data.decode())
        #print(f'Recebido de {client_address}: {message}')

        if message == "TIME":
            response_message = {"code": 1, "time":time}
        else:
            response_message = {"code": 0, "error_message":"Invalid Command"}
        
        response = json.dumps(response_message)
        client_socket.sendall(response.encode())
        
    client_socket.close()
    #print(f'Conexão com {client_address} encerrada')

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    #print(f'Servidor ouvindo em {host}:{port}')

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def start_client(clock_id, host, port):
    global clocks
    connected = False
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
            connected = True
            #print(f'Conectado ao servidor em {host}:{port}')
        except (socket.error, socket.timeout) as e:
            sleep(3)
            #print(f'Tentando conexão com {host}:{port}')

        while connected:
            message = json.dumps("TIME")
            try:
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
            except (socket.error, socket.timeout) as e:
                #print(f'Conexão com {host} encerrada')
                connected = False
                client_socket.close()
                break
            message = json.loads(data.decode())
            #print(f'Recebido do servidor: {message}')
            if message["code"] == 1:
                clocks[clock_id] = message["time"]
            else:
                print(message["error_message"])
            sleep(0.5)

def drift_time():
    global time
    global drift
    global entry_detection
    print(time)
    while True:
        sleep(drift)
        times = clocks.values()
        times_list = list(times)
        if len(times) > 0:
            time = max(times) + 1
        else:
            time = time + 1
        if not(entry_detection):
            clear_console()
            print(times_list)
            print(time)

# Limpa o console
def clear_console():
    # Verifica o sistema operacional e executa o comando apropriado
    if os.name == "posix": # Linux e macOS
        os.system("clear")
    elif os.name == "nt": # Windows
        os.system("cls")
    else:
        print("Não foi possível limpar a tela para este sistema.")

drift_time_thread = threading.Thread(target=drift_time)
drift_time_thread.start()

server_thread = threading.Thread(target=start_server, args=(host, port), daemon=True)
server_thread.start()

clock1_thread = threading.Thread(target=start_client, args=("1", host, port), daemon=True)
clock1_thread.start()

clock2_thread = threading.Thread(target=start_client, args=("2", clock2_host, clock2_port), daemon=True)
clock2_thread.start()

clock3_thread = threading.Thread(target=start_client, args=("3", clock3_host, clock3_port), daemon=True)
clock3_thread.start()

while True:
    input()
    entry_detection = True
    clear_console()
    drift = float(input("New  drift: "))
    entry_detection = False