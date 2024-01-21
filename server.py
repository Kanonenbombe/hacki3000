from flask import Flask, render_template
from flask_socketio import SocketIO
import socket
import threading
from collections import deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = {}



def client_handler(client_socket, client_address):
    # Initialisiere client_responses für diesen Client
    client_responses = deque(maxlen=5)

    while True:
        try:
            response = client_socket.recv(4096).decode()
            if response:
                formatted_address = f"{client_address[0]}-{client_address[1]}"
                client_responses.append(response)  # Antwort hinzufügen
                all_responses = '<br>'.join(client_responses)  # Alle Antworten als String
                socketio.emit('client_response', {'client': formatted_address, 'response': all_responses})
        except ConnectionResetError:
            break
    del clients[client_address]
    client_socket.close()

@app.route('/')
def index():
    return render_template('index.html', clients=list(clients.keys()))

@socketio.on('send_command')
def handle_command(data):
    client_info = data['client'].split('-')
    client_address = (client_info[0], int(client_info[1]))
    command = data['command']

    if client_address in clients:
        clients[client_address].send(command.encode())

def start_command_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        clients[addr] = client_socket
        client_thread = threading.Thread(target=client_handler, args=(client_socket, addr))
        client_thread.start()

if __name__ == '__main__':
    threading.Thread(target=start_command_server, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
