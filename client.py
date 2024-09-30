import socket
import time
import sys

# Function to start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_host = '127.0.0.1'  
    server_port = 12345         

    # Connect to the server
    client_socket.connect((server_host, server_port))
    client_hello = "Hello"
    
    for i in range(3):
        client_socket.send(client_hello.encode('utf-8'))
        time.sleep(2)
        server_acknowledgement = client_socket.recv(9).decode('UTF-8')
        if server_acknowledgement != "Hello ACK":
            continue
        if i > 3:
            return 404
        
    print("Connected to the server. Type 'exit' to end the connection.")

    try:
        while True:
            # Get user input for the message to send
            message = input("Enter message to send (type 'exit' to quit): ")
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            
            # If the message is 'exit', break out of the loop
            if message.lower() == 'exit':
                print("Exiting...")
                break

            # Receive and print the server's response
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Server replied: {data}")
    
    except KeyboardInterrupt:
        print("\nCtrl+C detected! Disconnecting from the server...")

    finally:
        # Close the socket connection
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
    if start_client() == 404:
        start_client()
