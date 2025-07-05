import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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
        print("Draw for this round")
        return in_score
    elif amirali == "rock" and mahdi == "paper":
        print("Mahdi won this round")
        in_score[1] = in_score[1] + 1
    elif  amirali == "rock" and mahdi == "scissors":
        print("AmirAli won this round")
        in_score[0] = in_score[0] + 1
    elif amirali == "paper" and mahdi == "scissors":
        print("Mahdi won this round")
        in_score[1] = in_score[1] +1
    elif amirali == "paper" and mahdi == "rock":
        print("AmirAli won this round")
        in_score[0] = in_score[0] + 1
    elif amirali == "scissors" and mahdi == "paper":
        print("AmirAli won this round")
        in_score[0] = in_score[0] + 1
    elif amirali == "scissors" and mahdi == "rock":
        print("Mahdi won this round")
        in_score[1] = in_score[1] + 1
    return in_score

score = [0,0]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))  # Bind the socket to the address and port
    s.listen()            # Start listening for incoming connections
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept() # Accept a new connection. conn is a new socket object, addr is client's address
    with conn:
        print(f"Connected by {addr}")
        while score[0] < 3 and score[1] < 3:
            amirali_choice = show_menu()
            mahdi_choice = conn.recv(1024) # Receive up to 1024 bytes of data
            print(f'you brought: {amirali_choice} -----',end=" ")
            print(f"Mahdi brought: {mahdi_choice.decode()}") # Decode bytes to string
            conn.sendall(amirali_choice.encode()) # Send the received data back (echo)
            new_score = scoring(amirali_choice, mahdi_choice.decode(), score)
            score = new_score
        
        if score[0] > score[1]:
            result = "AmirAli won"
        else:
            result = "Mahdi won"
        print(result)
        conn.sendall(result.encode()) # Send the received data back (echo)
        

            
    print("Client disconnected.")

