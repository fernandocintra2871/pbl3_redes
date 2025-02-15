import socket
import threading
import json
import os
from time import sleep

# Obtenção dos valores das variáveis de ambiente
host = os.environ.get("host")
port = 12001

clock2_host = os.environ.get("clock2_host")
clock2_port = 12001

clock3_host = os.environ.get("clock3_host")
clock3_port = 12001

# Variáveis globais
time = 0
drift = 1
clocks = {}
entry_detection = False

# Função para lidar com clientes conectados ao servidor
def handle_client(client_socket, client_address):
    global time
    #print(f'Conexão estabelecida com {client_address}')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = json.loads(data.decode())
        #print(f'Recebido de {client_address}: {message}')

        # Responde com o tempo atual se a mensagem recebida for "TIME"
        if message == "TIME":
            response_message = {"code": 1, "time": time}
        else:
            response_message = {"code": 0, "error_message": "Invalid Command"}
        
        response = json.dumps(response_message)
        client_socket.sendall(response.encode())
        
    client_socket.close()
    #print(f'Conexão com {client_address} encerrada')

# Função para iniciar o servidor
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    #print(f'Servidor ouvindo em {host}:{port}')

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# Função para iniciar o cliente e se conectar a um servidor de relógio
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

# Função para simular a deriva do tempo
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
        if not entry_detection:
            clear_console()
            print("Tempo dos Relogios Conectados")
            print(times_list)
            print("Relogio")
            print(time)

# Função para limpar o console
def clear_console():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
    else:
        print("Não foi possível limpar a tela para este sistema.")

# Inicializa a thread para simular a deriva do tempo
drift_time_thread = threading.Thread(target=drift_time)
drift_time_thread.start()

# Inicializa a thread do servidor
server_thread = threading.Thread(target=start_server, args=(host, port), daemon=True)
server_thread.start()

# Inicializa as threads dos clientes (relógios)
clock1_thread = threading.Thread(target=start_client, args=("1", host, port), daemon=True)
clock1_thread.start()

clock2_thread = threading.Thread(target=start_client, args=("2", clock2_host, clock2_port), daemon=True)
clock2_thread.start()

clock3_thread = threading.Thread(target=start_client, args=("3", clock3_host, clock3_port), daemon=True)
clock3_thread.start()

# Loop principal para ajustar a deriva manualmente
while True:
    input()
    entry_detection = True
    clear_console()
    drift = float(input("New drift: "))
    entry_detection = False
