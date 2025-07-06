import socket

HOST = '127.0.0.1' 
PORT = 65432    

def send_with_length(sock, message):
    """
    send message with its length 
    first lengh of it as a 4byte numer then actuall message
    """
    encoded = message.encode()
    length = len(encoded).to_bytes(4, 'big')  # 4 bytes length prefix
    sock.sendall(length + encoded)


def recv_with_length(sock):
    length_bytes = sock.recv(4)
    length = int.from_bytes(length_bytes, 'big')
    return sock.recv(length).decode()


def show_menu():
    print("****************************")
    print("choose your choice")
    print("1-rock")
    print("2-paper")
    print("3-scissors")
    choice = get_choice()
    return choice

def get_choice() -> str|None :
    choice = int(input())
    if choice == 1:
        return "rock"
    elif choice == 2:
        return "paper"
    elif choice == 3:
        return "scissors"
    else:
        print("invalid choice")
        show_menu()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # Connect to the server
    while True:
        mahdi_choice = show_menu()
        send_with_length(s,mahdi_choice)
        amirali_choice = recv_with_length(s)
        print(f'you brought {mahdi_choice} -----',end=" ")
        print(f"AmirAli brought: {amirali_choice}") 
        score = int(recv_with_length(s))
        if score == 3:
            break 
    
    # message = "Hello, server!"
    # s.sendall(message.encode()) # Send the message (encode to bytes)
    # print(f"Sent: {message}")
    result = recv_with_length(s)
    print(f"Received: {result}")

print("Connection closed.")