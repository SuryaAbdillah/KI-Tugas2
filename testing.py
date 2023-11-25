from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_key_pair():
    # Generate an RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get the public key
    public_key = private_key.public_key()
    
    # Serialize keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

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

# Example usage
# sender_private_key, sender_public_key = generate_key_pair()
# recipient_private_key, recipient_public_key = generate_key_pair()

# message = "Hello, asymmetric encryption!"

recipient_public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0DBUTG/+Qdczc9+oGGa4\nJY+EZjVd5P1a9CW9wfHLZGfyU8sgQimRpxt2XUfHMYh+DCo3HM8+ilXmMmXydpOy\nUlDp4ecc9hdNb/CEE15ZtkGNpk/m5/iIkRUaWkPDDlYtER0tAouAKEq79595Eeob\nyo/Mg+8Zbjslb3ncjUug1ujqYobaUYvBylDcb7Rauz/vx9Jbbf4xYq0I37Q39U+9\ntljEORwnf1ZlSnAOycavUGoeBBu1cih85gM6QNBkNH4GX8RfmZ574OF/FXjfzFZt\n1U2VLlABnFe3Zv2bk1elrvHdKoWy76ZuWz9P78V1cK+qchUq7L4bxdYCs1/yv8s4\nqwIDAQAB\n-----END PUBLIC KEY-----\n'
recipient_private_key = b'-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDQMFRMb/5B1zNz\n36gYZrglj4RmNV3k/Vr0Jb3B8ctkZ/JTyyBCKZGnG3ZdR8cxiH4MKjcczz6KVeYy\nZfJ2k7JSUOnh5xz2F01v8IQTXlm2QY2mT+bn+IiRFRpaQ8MOVi0RHS0Ci4AoSrv3\nn3kR6hvKj8yD7xluOyVvedyNS6DW6OpihtpRi8HKUNxvtFq7P+/H0ltt/jFirQjf\ntDf1T722WMQ5HCd/VmVKcA7Jxq9Qah4EG7VyKHzmAzpA0GQ0fgZfxF+Znnvg4X8V\neN/MVm3VTZUuUAGcV7dm/ZuTV6Wu8d0qhbLvpm5bP0/vxXVwr6pyFSrsvhvF1gKz\nX/K/yzirAgMBAAECggEAEe0HZSmDgBHSmViZtbgqhPltkgtoUU5LZZhWVXvHYpbc\ns8Bav7eqlfP0ZiXHDgnNqKh95Fon7WtmDdLfZLxk71eOO+hVgw8QmOHhzXUjTmEo\nnDhnDnRE9hEWGs2Y3wQmj0Gu3Xg7ibydoL23hAZfbDqjhnyw+N/Y4ldg2T241KhD\nvBC2KokSNkl1r0LFDRBWkMWzCyT4SqdOSWtmsScccWHY2i0VFCfXoDPdGT+3oVid\nted/+2MtFIEuA0T7Aredbyzh3z2BPqXn23+Tp62M87RE58MBz+i/Q26OkJ33BI3U\nYhqese2cR32eBiSAAXIWiFDvhfspjXluHXG8oI5p2QKBgQDpOlogHnzmzGND9RFg\ncdIq1UJj+8h7Ka4VyFLSlSlfqI42Ersg9hggGl3IOzZi3WL1a4LiD50N1uaiYPPq\n/0IH7bWv18/Z4yb+x4kAekEwzkRYWx3jWODOwPgOWcdxxiKFppJ0jK8BTwRoFWml\nX3la/L2cWYvVw7uef+iFL9+5VwKBgQDkhBx50GBYGEz0xBvdH8PkBKa/pzJVvxIN\nJNKrcNp9D9HNnaYm02uOLfZcpR5vg6qEzSqjE0h/c1vPVi0H2igSR6vU/zct5Isp\nXW61ZBV7ZONf79NeO7oWgV/I34iB0xYpMyc9/7ElDCThPYzYvA5YDz9Wu7jw09Sj\nIRmbpAPizQKBgQCl4Q7A0W5caPohF2hohAvK0ysJGccZcieS7ouZouVuV9/trZzS\ncLXv/1C8XQDtiDAeBX1tc1Vsxm/7BaH2fd5k7TjP/Fqkyd6uTxSt9kXvhIUvon67\neDdMVgsXidtEnHtpO3Pm2TiPYbfsn24oZKNXh3MEhNvkCfajYK3sLISeuQKBgQCK\nFrdqeRwvQAgJBRTda9uhR5pISE3neP38iVrxFNJDLrMWsIR+A9aD5YxxcapRstvx\nQlXYk8eElP5O7YFqtE7wtPTGUq9SgUAC8B39aQx+M3ofODqfQDJ0dRuftEy2Pwuu\nO+Yj1gaDH7KNlfct5X45goVA8VGR3kApj8/8uIFMpQKBgQDPufvbTF/zBq+qpxZh\nZd9lhFYHV+FnJtAfMNRkQEi+6/wv3S9URfQ+6LF9o0HU33pBixq/EwCAqd87lYVG\nkeiNS6ipw9uMX+FdqcipguGysQlBtq4i4oI1Krdmxw0wVMBPzfKBipaBhl9BmGcA\n1f1twq9E9LvJdINO+MGp+YZHOQ==\n-----END PRIVATE KEY-----\n'
message = b'f3Pza0KkCjxaQn9yHVmNtWbftmItFI03ijBHy3SVDQ4='

# Encrypt the message using the recipient's public key
print("PUBLIC KEY\n", recipient_public_key)
print("PRIVATE KEY\n", recipient_private_key)

encrypted_message = encrypt(message, recipient_public_key)
encrypted_message = b'\xcf\x92y\xe2<\xf3X\xa0\x8f\x16\x98\xeedx\x91A(\xb1\x05^,\xd2\x9d\xd2/S\xf8\xac\xc4h\x86g\xc9;/\x19\xf2\x10\xd86G\x1d\xcaV\xcf\xef\xb1\xe2\x9d\x9c\n~\xbe[k\x8a\xc0#upP\x03p\xeeQ\xfd\t\x87WH;\xa51\x83Vr)p~\xfajw\xde\x98Q\xd0\x93<\x10\r\xa9k`\xa3\x9e]\x9d\x1a\xd1nm\xab\x91\xf7\xc6\x11E\xdft\xfd\x1e\x84aOo\xcd\xfb\xb6\xf7\xe1f8\x85\x83\x15\r\x1a~\xd0\xad\xba\xdcS,\ni\xb4\xf8\xfb\xda\xa6ppU4&\x11,G\xf5\x866\xd5TS\x02\xa9\xb3\x10\x8d{\xbd \x05\x17\xa9\x90\x80v\xa6v\x02\xc6g\xac$\xd7x\xd8\xcb\x85\xd6\x94\xe6p\xdb\xe6$\x99\xb86\xf1wZ\x94\x16.`=0m\xbac\xef\xf1m\xc5\x07\xaapbvh`\xae\xb9(=@x\xef\xc7Z\xe6\x98\xc2Hc\xa8ws\t\x18\x08@\xcd\xe55\x1ak~G0\xf1c\xd2u\x1c\xb2C\xc9n`~a4'

# Decrypt the message using the recipient's private key
decrypted_message = decrypt(encrypted_message, recipient_private_key)

print(f"Original Message: {message}")
print(f"Decrypted Message: {decrypted_message.encode()}")

print(f"Encrypted Message: {encrypted_message}")
