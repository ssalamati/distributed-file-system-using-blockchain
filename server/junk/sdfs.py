import socket
import threading
import hashlib


# Set the chunk size
CHUNK_SIZE = 1024 * 1024

# Define the number of replicas
REPLICA_COUNT = 3

# Define the IP addresses of the nodes
NODE_IPS = [
    '192.168.56.11',
    '192.168.56.12',
    '192.168.56.13',
    '192.168.56.14',
    '192.168.56.15'
]

# Define the port number for the server
SERVER_PORT = 12345

# Define the directory to store the files
STORAGE_DIR = '/tmp/myfs/'


class SDFS:
    def __init__(self, db):
        self.db = db
        self.server_thread = None

    def run_server(self):
        threading.Thread(target=self.start_server).start()

    def handle_client(self, conn, addr):
        print(f'Client connected from {addr}')

        try:
            # Receive the file name and file size
            rec = conn.recv(1024)
            print(rec)
            file_name = rec.decode()

            print(file_name)
            file_size = int(conn.recv(1024).decode())

            # Create a SHA256 hash object
            hash_object = hashlib.sha256()

            # Open a new file for writing
            file_path = STORAGE_DIR + file_name
            with open(file_path, 'wb') as f:
                # Receive the file data in chunks and write to the file
                data = conn.recv(CHUNK_SIZE)
                while data:
                    f.write(data)
                    hash_object.update(data)
                    data = conn.recv(CHUNK_SIZE)

            # Print the SHA256 hash of the file
            print(f'File received: {file_name}, SHA256 hash: {hash_object.hexdigest()}')

            # Replicate the file to the other nodes
            for i in range(REPLICA_COUNT - 1):
                node_ip = NODE_IPS[(NODE_IPS.index(addr[0]) + i + 1) % len(NODE_IPS)]
                self.replicate_file(file_path, node_ip)

        except Exception as e:
            print(f'Error handling client connection: {e}')

        finally:
            # Close the connection
            conn.close()
            print(f'Connection closed from {addr}')

    # @staticmethod
    # def replicate_file(file_path, node_ip):
    #     try:
    #         # Connect to the node and send the file name and file size
    #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #             s.connect((node_ip, SERVER_PORT))
    #             s.sendall(file_path.encode())
    #             s.sendall(str(-1).encode())
    #
    #             # Open the file and send the file data in chunks
    #             with open(file_path, 'rb') as f:
    #                 data = f.read(CHUNK_SIZE)
    #                 while data:
    #                     s.sendall(data)
    #                     data = f.read(CHUNK_SIZE)
    #
    #         print(f'File replicated to node {node_ip}')
    #
    #     except Exception as e:
    #         print(f'Error replicating file to node {node_ip}: {e}')

    def start_server(self):
        # Create the storage directory if it does not exist
        import os
        if not os.path.exists(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)

        # Create a socket and start listening for connections
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', SERVER_PORT))
            s.listen()

            print(f'Server listening on port {SERVER_PORT}')

            while True:
                # Wait for a client to connect and handle the connection in a new thread
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()


