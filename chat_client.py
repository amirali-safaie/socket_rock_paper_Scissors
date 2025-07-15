import socket

SERVER_HOST = '127.0.0.1' # <--- CHANGE THIS!
SERVER_PORT = 65432 # Must match server port

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to chat server at {SERVER_HOST}:{SERVER_PORT}")
            print("Type your messages. Type 'quit' to end.")

            while True:
                # 1. Send your message to friend
                your_message = input("You: ")
                s.sendall(your_message.encode('utf-8'))
                if your_message.lower() == 'quit':
                    print("You quit the chat.")
                    break

                # 2. Receive message from friend
                friend_message_bytes = s.recv(1024)
                if not friend_message_bytes:
                    print("Friend disconnected.")
                    break
                
                friend_message = friend_message_bytes.decode('utf-8')
                if friend_message.lower() == 'quit':
                    print("Friend quit the chat.")
                    break
                print(f"Friend: {friend_message}")

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running on {SERVER_HOST}:{SERVER_PORT} and firewall open?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Client closing.")

if __name__ == "__main__":
    start_client()