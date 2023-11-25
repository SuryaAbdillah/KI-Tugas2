from cryptography.fernet import Fernet

def encrypt_file(file_data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(file_data)
    return encrypted_data

def decrypt_file(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data

