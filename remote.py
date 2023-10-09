import json
import socket
import subprocess
import os
import sys
import time

from dotenv import load_dotenv

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 65432

# Store the PID of the running bot process

def start_bot(connection):
    try:
        process = subprocess.Popen(['start', 'cmd', '/c', 'start_bot.bat'], shell=True)
        # Wait for the process to start
        time.sleep(10)  # Adjust this delay as needed')
        load_dotenv(override=True)
        botPID = os.getenv('PID')
        connection.sendall(f"Bot started with PID: {botPID}".encode())
        print(f"Successfuly started the bot with Process ID: {botPID}")

    except Exception as e:
        print(f'Failed to start the bot. Error: {str(e)}')


def stop_bot(connection):
    load_dotenv(override=True)

    try:
        botPID = os.getenv('PID')
        # Terminate the process using its PID
        os.system(f"taskkill /F /PID {botPID}")
        connection.sendall(f"Bot with PID {botPID} has been stopped.".encode())
        print(f'Bot with PID {botPID} stopped successfully.')
        

    except Exception as e:
        print(f'An error occurred while stopping the bot: {str(e)}')

def restart(connection):
    print("Initiating a restart.")
    stop_bot(connection)

    with open('./config.json', 'r') as f:
        config = json.load(f)

    config['Restarted'] = "True"

    with open('./config.json', 'w') as f:
        json.dump(config, f)

    start_bot(connection)

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
server_socket.listen(1)

os.system('cls')
print('Server is listening for incoming connections...')

def main_loop():
    while True:
        try:

            connection, client_address = server_socket.accept()
            print('Connection established with:', client_address)

            data = connection.recv(1024).decode()
            if data == 'start':
                connection.sendall('Please standby, bot is starting.'.encode())
                start_bot(connection)
                connection.sendall('Bot started.'.encode())

            elif data == 'stop':
                connection.sendall('Please standby, bot is stopping.'.encode())
                stop_bot(connection)
                connection.sendall('Bot has stoped'.encode())

            elif data == 'restart':
                connection.sendall('Please standby, bot is restarting.'.encode())
                restart(connection)
                connection.sendall('Restarting'.encode())
            elif data == 'exit':
                connection.sendall('Disconnecting, please wait.'.encode())
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            print('Restating the server...')
            python = sys.executable
            os.execl(python, python, * sys.argv)
        except ConnectionResetError as e:
            print(f'Client connection reset: {str(e)}') 

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Server was interrupted by the user.")