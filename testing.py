import os
import base64

# Generate a random 32-byte key
random_key = os.urandom(32)

# Encode the key in base64
encoded_key = base64.b64encode(random_key).decode('utf-8')

print("Generated Key:", random_key)
print("Base64 Encoded Key:", encoded_key)
