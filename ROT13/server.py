import socket
import threading
from codecs import encode, decode

HOST = 'localhost'
PORT = 8000
SOCKET_TIMEOUT = 90

# This function handles reading data sent by a client.
# Repeatedly sends back a ROT13 encoded string unless the client sends a ROT13
# encoded string saying "Send Flag", in which ase a ROT13 encoded flag is returned.
# The connection is closed in case of timeout (90s) or "quit" command
# This function is meant to be started in a separate thread (one thread per client)
def handle_client(client_connection, client_address):

    # Setup socket timeout
    client_connection.settimeout(SOCKET_TIMEOUT)

    try:
        while True:
            # Define the initial string to be encoded and sent back to the client.
            s = "To receive the flag, respond with ROT13 encoded text saying 'Send Flag'\n"
            enc_s = encode(s, 'rot13')
            client_connection.send(enc_s.encode('utf-8'))

            # Receive data from client
            data = client_connection.recv(1024)

            print('Received from:- {}:{} - {}'.format(client_address[0], client_address[1], data))

            # Decode the received data from binary to text and then rot-13 decode it.
            d = data.decode('utf-8')
            decoded = decode(d, 'rot13')

            # Check if the response is what we expect
            if decoded == "Send Flag\n" or decoded == "Send Flag\r\n":

                # Encode the flag and send it.
                s = 'Flag{Well_Done_You_Speak_ROT13}\n'
                enc_s = encode(s, 'rot-13')

                client_connection.send(enc_s.encode('utf-8'))
                break

            # Close connection if "quit" received from client
            if data == b'quit\r\n' or data == b'quit\n':
                print('Client IP:- {}:{} disconnected'.format(client_address[0], client_address[1]))
                client_connection.shutdown(1)
                client_connection.close()
                break

    # Timeout and close connection after 30s of inactivity
    except socket.timeout:
        print('Client IP:- {}:{} timed out'.format(client_address[0], client_address[1]))
        client_connection.send("Timeout. Closing connection\n".encode('utf-8'))
        client_connection.shutdown(1)
        client_connection.close()


# This function opens a socket and listens on specified port. As soon as a
# connection is received, it is transferred to another socket so that the main
# socket is not blocked and can accept new clients.
def listen(host, port):
    # Create the main socket (IPv4, TCP)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((host, port))

    # Listen for clients (max 10 clients in waiting)
    connection.listen(10)

    # Every time a client connects, allow a dedicated socket and a dedicated
    # thread to handle communication with that client without blocking others.
    # Once the new thread has taken over, wait for the next client.
    while True:
        current_connection, client_address = connection.accept()

        print('Client IP:- {}:{} connected'.format(client_address[0], client_address[1]))

        handler_thread = threading.Thread(target=handle_client,
                                          args=(current_connection,
                                                client_address))

        # daemon makes sure all threads are killed if the main server process
        # gets killed
        handler_thread.daemon = True
        handler_thread.start()


if __name__ == "__main__":
    try:
        print("Server Starting on {}:{}".format(HOST,PORT))
        listen(HOST, PORT)

    except KeyboardInterrupt:
        print('Exiting Server')
        pass
