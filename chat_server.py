import socket

HOST = '0.0.0.0' # Listen on all interfaces
PORT = 65432     # Port to use

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for friend to connect...")

        conn, addr = s.accept()
        with conn:
            print(f"Friend connected from {addr}")
            print("Type your messages. Type 'quit' to end.")

            while True:
                # 1. Receive message from friend
                friend_message_bytes = conn.recv(1024)
                if not friend_message_bytes:
                    print("Friend disconnected.")
                    break
                friend_message = friend_message_bytes.decode('utf-8')
                if friend_message.lower() == 'quit':
                    print("Friend quit the chat.")
                    break
                print(f"Friend: {friend_message}")

                your_message = input("You: ")
                conn.sendall(your_message.encode('utf-8'))
                if your_message.lower() == 'quit':
                    print("You quit the chat.")
                    break

    print("Server closing.")

if __name__ == "__main__":
    start_server()