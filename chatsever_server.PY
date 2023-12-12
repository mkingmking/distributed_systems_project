import socket
import threading
import os as os
import sqlite3
from datetime import datetime


HOST_IP = socket.gethostbyname(socket.gethostname())  
HOST_PORT = 90
ENCODER = "utf-8"
BYTESIZE = 1024


# Dictionary 
clients = {}
nicknames = {}
dns_table = {}  


def initialize_database():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (timestamp TEXT, nickname TEXT, message TEXT)''')
    conn.commit()
    conn.close()

def save_message(nickname, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", (timestamp, nickname, message))
    conn.commit()
    conn.close()


def broadcast(message, sender="Server"):
    full_message = f"{sender}: {message}".encode(ENCODER)
    for client_socket in clients.values():
        client_socket.send(full_message)


def handle_client(client_socket):
    while True:
        try:
            
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            nickname = nicknames[client_socket]

            # database integration
            save_message(nickname, message)

            if message.lower() == "quit":
                broadcast(f"{nickname} has left the chat.", "Server")
                print(f"{nickname} has left the chat.")
                break

            
            if message.startswith("@"):
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    recipient = parts[0][1:]
                    if recipient in clients:
                        private_message = f"{nickname} (private): {parts[1]}"
                        clients[recipient].send(private_message.encode(ENCODER))
                    else:
                        client_socket.send(f"User '{recipient}' not found.".encode(ENCODER))
                continue  

            else:
                full_message = f"{nickname}: {message}"
                print(full_message)  
                broadcast(message, nickname)
        except ConnectionResetError:
            print(f"{nickname} has disconnected.")
            break  
        except Exception as e:
            print(f"An error occurred: {e}")
            break 

    # Client disconnect olursa:
    clients.pop(nickname, None)
    nicknames.pop(client_socket, None)
    dns_table.pop(nickname, None)  
    client_socket.close()



# Server Socketini açıyoruz.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

print("Server is running and listening for connections...\n")

# Main Döngü

initialize_database()

print("basarili")
try:
    while True:
        def send_server_message():
            while True:
                message = input()  
                if message.lower() == "quit":
                    print("Server is shutting down...")
                    os._exit(1)  
                broadcast(message, "Server")
        
        client_socket, client_address = server_socket.accept()

        
        nickname = client_socket.recv(BYTESIZE).decode(ENCODER)
        nicknames[client_socket] = nickname
        clients[nickname] = client_socket
        dns_table[nickname] = client_socket  

        print(f"Accepted new connection from {client_address} with nickname: {nickname}")
        broadcast(f"{nickname} has joined the chat!")

        
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
        
        server_message_thread = threading.Thread(target=send_server_message)
        server_message_thread.start()

except KeyboardInterrupt:
    print("\nServer is shutting down...")
finally:
    server_socket.close()
