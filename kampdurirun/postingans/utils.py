from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def encrypt_file(file_data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(file_data)
    return encrypted_data

def decrypt_file(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data


def encrypt(message, recipient_public_key):
    # Load the recipient's public key
    recipient_key = serialization.load_pem_public_key(recipient_public_key, backend=default_backend())
    
    # Encrypt the message
    ciphertext = recipient_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return ciphertext

def decrypt(ciphertext, recipient_private_key):
    # Load the recipient's private key
    private_key = serialization.load_pem_private_key(recipient_private_key, password=None, backend=default_backend())
    
    # Decrypt the message
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return plaintext.decode('utf-8')