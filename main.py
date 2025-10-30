#!/usr/bin/env python3
"""
Encrypted QR Code Generator
Generates a QR code from encrypted text input
"""

import qrcode
from cryptography.fernet import Fernet
import os

def generate_key():
    """Generate and save encryption key"""
    key = Fernet.generate_key()
    with open('key.txt', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load encryption key from file"""
    if os.path.exists('key.txt'):
        with open('key.txt', 'rb') as key_file:
            return key_file.read()
    return None

def encrypt_text(text, key):
    """Encrypt text using Fernet symmetric encryption"""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    return encrypted

def decrypt_text(encrypted_text, key):
    """Decrypt text using Fernet symmetric encryption"""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_text)
    return decrypted.decode()

def generate_qr_code(data, filename='output.png'):
    """Generate QR code from data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

def main():
    # Read input text
    try:
        with open('input.txt', 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return
    
    # Generate or load encryption key
    key = load_key()
    if key is None:
        print("Generating new encryption key...")
        key = generate_key()
    else:
        print("Using existing encryption key...")
    
    # Encrypt the text
    encrypted_text = encrypt_text(text, key)
    print(f"Text encrypted successfully")
    
    # Generate QR code from encrypted text
    generate_qr_code(encrypted_text.decode('latin-1'))
    print("\nProcess complete!")
    print(f"- Encryption key: key.txt")
    print(f"- QR code: output.png")
    print(f"\nNote: Keep key.txt safe to decrypt the QR code later!")

if __name__ == "__main__":
    main()
