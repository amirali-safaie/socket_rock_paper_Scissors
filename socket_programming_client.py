import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def show_menu():
    print("****************************")
    print("choose your choice")
    print("1-rock")
    print("1-paper")
    print("1-scissors")
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
        s.sendall(mahdi_choice.encode()) # Send the received data back (echo)
        amirali_choice = s.recv(1024) # Receive up to 1024 bytes of data
        print(f'you brought {mahdi_choice} -----',end=" ")
        print(f"AmirAli brought: {amirali_choice.decode()}") # Decode bytes to string
    
    # message = "Hello, server!"
    # s.sendall(message.encode()) # Send the message (encode to bytes)
    # print(f"Sent: {message}")
    # data = s.recv(1024) # Receive response from server
    # print(f"Received: {data.decode()}")

print("Connection closed.")