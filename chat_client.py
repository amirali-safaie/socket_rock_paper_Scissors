import socket
import threading

SERVER_HOST = '127.0.0.1' # <--- CHANGE THIS!
SERVER_PORT = 65432 # Must match server port
breaker = False


def recciver(conn, recciver_breaker):
    friend_message_bytes = conn.recv(1024)
    if not friend_message_bytes:
        print("Friend disconnected.")
        recciver_breaker = True
    friend_message = friend_message_bytes.decode('utf-8')
    if friend_message.lower() == 'quit':
        print("Friend quit the chat.")
        recciver_breaker = True
    print()
    print(f"Friend: {friend_message}")


def sender(conn, sender_breaker):
    your_message = input("You: ")
    conn.sendall(your_message.encode('utf-8'))
    if your_message.lower() == 'quit':
        print("You quit the chat.")
        sender_breaker = True
    

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to chat server at {SERVER_HOST}:{SERVER_PORT}")
            print("Type your messages. Type 'quit' to end.")

            while True:

                reccive_thread = threading.Thread(target=recciver, args=(s, breaker))
                sender_thread = threading.Thread(target=sender, args=(s, breaker))

                reccive_thread.start()
                sender_thread.start()

                reccive_thread.join()
                sender_thread.join()
                
                if breaker is True:
                    break

        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running on {SERVER_HOST}:{SERVER_PORT} and firewall open?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Client closing.")

if __name__ == "__main__":
    start_client()