from Crypto.Cipher import AES

AES_KEY = b'0123456789abcdef'  # Must match the encryption key
BLOCK_SIZE = 16  # AES block size

def unpad(data):
    """Remove PKCS7 padding."""
    pad_len = data[-1]
    return data[:-pad_len]

def decrypt_and_execute(input_file):
    with open(input_file, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    # Remove padding
    decrypted_data = unpad(decrypted_data)

    exec(decrypted_data.decode("utf-8"))

decrypt_and_execute("bot_core_enc.py")