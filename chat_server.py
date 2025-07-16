import socket
import threading

HOST = '0.0.0.0' # Listen on all interfaces
PORT = 65432     # Port to use
breaker = False


def recciver(sock, stop_event):
    receiver_instance = MessageReceiver(sock) # Assuming MessageReceiver is defined
    while not stop_event.is_set(): # Loop as long as stop_event is NOT set
        try:
            message_bytes = receiver_instance.receive_message()
            if message_bytes is None: # Timeout, check stop_event again
                continue
            if not message_bytes: # Connection closed by peer
                print("\nFriend disconnected.")
                stop_event.set() # Signal stop
                break
            
            message = message_bytes.decode('utf-8')
            if message.lower() == 'quit':
                print("\nFriend quit the chat.")
                stop_event.set() # Signal stop
                break
            print(f"\nFriend: {message}")
            print("You: ", end="", flush=True) # Reprint prompt for sender
        except Exception as e:
            print(f"[RECEIVER ERROR] {e}")
            stop_event.set() # Signal stop on error
            break
    print("Receiver thread exiting.")


def sender(sock, stop_event):
    while not stop_event.is_set(): # Loop as long as stop_event is NOT set
        try:
            message = input("You: ")
            if message.lower() == 'quit':
                sock.sendall(message.encode('utf-8') + b'\n') # Send quit message
                stop_event.set() # Signal other threads/main to stop
                break # Exit sender loop
            sock.sendall(message.encode('utf-8') + b'\n')
        except Exception as e:
            print(f"[SENDER ERROR] {e}")
            stop_event.set() # Signal stop on error
            break
    print("Sender thread exiting.")
    


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for friend to connect...")

        conn, addr = s.accept()
        with conn:
            print(f"Friend connected from {addr}")
            print("Type your messages. Type 'quit' to end.")

            reccive_thread = threading.Thread(target=recciver, args=(conn, breaker))
            sender_thread = threading.Thread(target=sender, args=(conn, breaker))

            while True:

                reccive_thread.start()
                sender_thread.start()
                
                reccive_thread.c
                if breaker is True:
                    break

    print("Server closing.")

if __name__ == "__main__":
    start_server()