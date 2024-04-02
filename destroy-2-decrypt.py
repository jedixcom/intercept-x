#! "C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env\Scripts\python"
# Decryptor - Offensive Programming - Blok3

from cryptography.fernet import Fernet
import os

def load_key(key_file_path):
    """Load the encryption key."""
    with open(key_file_path, 'rb') as keyfile:
        key = keyfile.read()
    return key

def decrypt_file(file_path, cipher_suite):
    """Decrypt a file using Fernet symmetric encryption."""
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
        # Decrypt data
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        # Schrijf Terug
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def decrypt_directory(directory_path, cipher_suite):
    """Recursively decrypt each file in the directory and its subdirectories."""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, cipher_suite)
            print(f"Decrypted {file_path}")

# Laad de key vanuit File
key = load_key("encryption_key.key")

# Initeer een fernet crypto met sleutel
cipher_suite = Fernet(key)

# Direcorty om te decrypten (deze moet overeenkomen met directory in ecrypt script)
directory_to_decrypt = "encrypt-this"
decrypt_directory(directory_to_decrypt, cipher_suite)

print("Decryption complete. Check your files.")
