import socket
import threading
import sys
#variable List
Name = ""

server_details = {Name:"MsgBuddy"}
# List to keep track of all connected client sockets
client_sockets = []

# Function to handle each client connection
def handle_client(client_socket, client_address):
    global client_sockets

    print(f"Connection from {client_address} has been established!")

    try:
        while True:
            client_hello = client_socket.recv(1024).decode('utf-8')
            if client_hello != "Hello":
                continue
            server_ack = "Hello ACK"
            client_socket.send(server_ack.encode('utf-8'))

            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            
            if not data:
                break  # Client disconnected or connection error

            print(f"Client {client_address} sent: {data}")

            # If the client sends 'exit', close the connection
            if data.lower() == 'exit':
                print(f"Client {client_address} requested to close the connection.")
                break

            # Send a response back to the client
            response = f"Hello {data}"
            client_socket.send(response.encode('utf-8'))
    
    except ConnectionResetError:
        print(f"Connection with {client_address} was reset.")
    finally:
        # Close the connection with the client
        client_socket.close()
        client_sockets.remove(client_socket)
        print(f"Connection from {client_address} closed.")

# Main function to start the server
def start_server():
    global server_socket
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and port
    host = '127.0.0.1'  
    port = 12345        

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)  # Listen for up to 5 connections
    print(f"Server is listening on {host}:{port}")

    try:
        while True:
            # Accept an incoming connection
            client_socket, client_address = server_socket.accept()
            
            # Add client socket to the list for proper shutdown
            client_sockets.append(client_socket)

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\nCtrl+C detected! Shutting down the server...")

    finally:
        # Close the server socket
        server_socket.close()
        print("Server socket closed.")

        # Close all client sockets
        for sock in client_sockets:
            sock.close()
            print("Closed a client socket.")

        # Exit the program
        sys.exit(0)

if __name__ == "__main__":
    start_server()
