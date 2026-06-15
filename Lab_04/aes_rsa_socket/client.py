from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345)) # Note: server_address

# Generate RSA key pair for client
client_key = RSA.generate(2048)

# Receive server's public key
server_public_key = RSA.import_key(client_socket.recv(2048))

# Send client's public key to server
client_socket.send(client_key.publickey().export_key(format='PEM'))

# Receive encrypted AES key from server
encrypted_aes_key = client_socket.recv(256)

# Decrypt AES key using client's private key
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to receive messages from server
def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"\nReceived: {decrypted_message}")
        except:
            print("Connection closed by server")
            break

# Start thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main loop to send messages
while True:
    message = input("Enter message (type 'exit' to quit): ")
    if message == 'exit':
        break
    encrypted_message = encrypt_message(aes_key, message)
    client_socket.send(encrypted_message)

client_socket.close()