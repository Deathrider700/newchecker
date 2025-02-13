from Crypto.Cipher import AES
import os

AES_KEY = b'0123456789abcdef'  # Keep this key secure!
BLOCK_SIZE = 16  # AES block size (16 bytes)

def pad(data):
    """Pad data using PKCS7 to be a multiple of 16 bytes."""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def encrypt_file(input_file, output_file):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    
    with open(input_file, "rb") as f:
        data = pad(f.read())

    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(output_file, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)

    print(f"✅ Encrypted: {output_file}")

encrypt_file("bot_core.py", "bot_core_enc.py")