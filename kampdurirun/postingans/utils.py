from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from PyPDF2 import PdfReader, PdfWriter
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import io
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def sign_pdf(pdf_data, private_key):
    # Load private key
    private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

    # Create a signature
    signature = private_key.sign(
        pdf_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Create a PDF with the original content and the signature
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 100, "Original PDF Content")
    can.save()

    # Rewind the BytesIO buffer to the beginning before writing
    packet.seek(0)

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(io.BytesIO(pdf_data))

    output = PdfWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Sign the PDF
    output.sign(signature)

    # Create a new BytesIO buffer to store the final PDF with the signature
    signed_pdf_buffer = io.BytesIO()
    output.write(signed_pdf_buffer)

    return signed_pdf_buffer.getvalue()

def verify_signature(pdf_data, signature, recipient_public_key):
    # Load public key
    public_key = serialization.load_pem_public_key(recipient_public_key, backend=default_backend())

    # Create a PDF reader
    pdf_reader = PdfReader(pdf_data)

    # Calculate the hash of the PDF content
    pdf_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pdf_hash.update(pdf_data)
    digest = pdf_hash.finalize()

    try:
        # Verify the signature using the public key
        public_key.verify(signature, digest, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False
