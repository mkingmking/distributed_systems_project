import streamlit as st
import socket
import threading

# Global variables to store messages and control the receive thread
received_messages = []
keep_receiving = True

def receive_messages(sock):
    global received_messages, keep_receiving
    while keep_receiving:
        try:
            message = sock.recv(1024).decode("utf-8")
            if message:
                received_messages.append(message)
        except:
            keep_receiving = False

# Streamlit interface
st.title("Chatsever")

nickname = st.sidebar.text_input("Nickname", value="Misafir")
server_ip = st.sidebar.text_input("Server IP", value="192.168.87.104")
server_port = st.sidebar.number_input("Server Port", value=90, step=1)
message = st.text_input("Your Message")

if st.button("Connect"):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        client_socket.send(nickname.encode("utf-8"))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        st.success("Connected to the server.")
    except Exception as e:
        st.error(f"Failed to connect: {e}")

if st.button("Send"):
    if client_socket:
        client_socket.send(message.encode("utf-8"))
        st.text_input("Your Message", value="", key="1")  # Reset message input

st.write("Messages:")
for msg in received_messages:
    st.text(msg)

# This part ensures the thread is closed when the app is rerun or closed
if 'client_socket' in globals():
    keep_receiving = False
    client_socket.close()
