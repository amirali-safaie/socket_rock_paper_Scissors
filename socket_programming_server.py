import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def send_with_length(sock, message):
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

def scoring(amirali, mahdi, in_score):
    if amirali == mahdi:
        return in_score
    elif amirali == "rock" and mahdi == "paper":
        in_score[1] = in_score[1] + 1
    elif  amirali == "rock" and mahdi == "scissors":
        in_score[0] = in_score[0] + 1
    elif amirali == "paper" and mahdi == "scissors":
        in_score[1] = in_score[1] +1
    elif amirali == "paper" and mahdi == "rock":
        in_score[0] = in_score[0] + 1
    elif amirali == "scissors" and mahdi == "paper":
        in_score[0] = in_score[0] + 1
    elif amirali == "scissors" and mahdi == "rock":
        in_score[1] = in_score[1] + 1
    return in_score

score = [0,0]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))  
    s.listen()            
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while score[0] < 3 and score[1] < 3:
            amirali_choice = show_menu()
            mahdi_choice = recv_with_length(conn)
            print(f'you brought: {amirali_choice} -----',end=" ")
            print(f"Mahdi brought: {mahdi_choice}") 
            send_with_length(conn,amirali_choice)
            new_score = scoring(amirali_choice, mahdi_choice, score)
            score = new_score
            send_with_length(conn, str(max(score)))
        
        if score[0] > score[1]:
            result = "AmirAli won"
        else:
            result = "Mahdi won"
        print(result)
        send_with_length(conn, result)
        

            
    print("Client disconnected.")

