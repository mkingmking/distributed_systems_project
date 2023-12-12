import socket
import threading

DEST_IP = "192.168.87.104"  
DEST_PORT = 90
ENCODER = "utf-8"
BYTESIZE = 1024


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(BYTESIZE).decode(ENCODER)
            if not message:
                continue
            if message == "quit":
                print("\nServer has closed the connection.")
                sock.close()
                break
            else:
                print(f"\n{message}")
        except ConnectionResetError:
            print("\nConnection lost to server.")
            break
        except OSError:
            break  # Hata durumunda Socketi kapat.


def send_messages(sock):
    try:
        while True:
            message = input()
            if message.lower() == "quit":
                sock.send("quit".encode(ENCODER))
                break
            sock.send(message.encode(ENCODER))
    except KeyboardInterrupt:
        sock.send("quit".encode(ENCODER))


nickname = input("Enter your nickname: ")

# CSocket aciliyor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))

# Nickname secimi
client_socket.send(nickname.encode(ENCODER))

# Receive ve send icin ayri threadlari aciyoruz.
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client_socket,))
send_thread.start()

# İki thread programin bitmesi icin birbirini bekliyor.
receive_thread.join()
send_thread.join()
print("Exited the chat.")
