import base64
import zlib
import marshal
import hashlib
import bz2
import gzip
import os
from Crypto.Cipher import AES, Blowfish, DES, ARC4
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA3_256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from cryptography.fernet import Fernet
from xxtea import encrypt as xxtea_encrypt
import codecs
import string
import cfonts
from termcolor import colored

# Print welcome message
cfonts.say("Encryption Tool", font="block", colors=["cyan"])
print(colored("Welcome to the Encryption Tool! Choose your method wisely! 🔒", 'green'))

# Password check
def password_check():
    password = input(colored("Enter the password to proceed: ", 'blue'))
    return password == "Ethical"

# Method Menu
def method_menu():
    print("\nAvailable Methods:")
    print(colored("1. AES Encryption", 'yellow'))
    print(colored("2. Blowfish Encryption", 'yellow'))
    print(colored("3. DES Encryption", 'yellow'))
    print(colored("4. RC4 Encryption", 'yellow'))
    print(colored("5. Fernet Encryption", 'yellow'))
    print(colored("6. XXTEA Encryption", 'yellow'))
    print(colored("7. RSA Encryption", 'yellow'))
    print(colored("8. XOR Encryption", 'yellow'))
    print(colored("9. GZIP Compression", 'yellow'))
    print(colored("10. BZIP2 Compression", 'yellow'))
    print(colored("11. Zlib Compression", 'yellow'))
    print(colored("12. Marshal Serialization", 'yellow'))
    print(colored("13. ROT13 Encryption", 'yellow'))
    print(colored("14. Caesar Cipher (Shift Cipher)", 'yellow'))
    print(colored("15. HMAC", 'yellow'))
    print(colored("16. SHA3-256 Hashing", 'yellow'))
    print(colored("17. PBKDF2 Key Derivation", 'yellow'))
    print(colored("18. Chain Multiple Methods", 'yellow'))
    print(colored("19. Encode with Base64", 'yellow'))
    print(colored("20. Encode with Base16", 'yellow'))

# AES Encryption
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext

# AES Decryption
def aes_decrypt(data, key):
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext)

# Base64 Encryption
def base64_encrypt(data):
    return base64.b64encode(data)

# zlib Compression
def zlib_encrypt(data):
    return zlib.compress(data)

# BZIP2 Compression
def bzip2_encrypt(data):
    return bz2.compress(data)

# GZIP Compression
def gzip_encrypt(data):
    return gzip.compress(data)

# Marshal Serialization
def marshal_encrypt(data):
    return marshal.dumps(data)

# ROT13 Encryption
def rot13_encrypt(data):
    return codecs.encode(data, 'rot_13')

# Hashing functions (MD5, SHA1, SHA256, SHA512, SHA3-256)
def hash_md5(data):
    return hashlib.md5(data.encode()).hexdigest()

def hash_sha1(data):
    return hashlib.sha1(data.encode()).hexdigest()

def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def hash_sha512(data):
    return hashlib.sha512(data.encode()).hexdigest()

def hash_sha3_256(data):
    return SHA3_256.new(data.encode()).hexdigest()

# Caesar Cipher (Shift Cipher)
def caesar_cipher_encrypt(text, shift):
    shift = shift % 26
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)

# Blowfish Encryption
def blowfish_encrypt(data, key):
    cipher = Blowfish.new(key, Blowfish.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext

# Blowfish Decryption
def blowfish_decrypt(data, key):
    nonce = data[:8]  # Blowfish nonce size is smaller
    ciphertext = data[8:]
    cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext)

# XOR Encryption
def xor_encrypt(data, key):
    return bytes([b ^ key for b in data])

# RC4 Encryption
def rc4_encrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

# RC4 Decryption
def rc4_decrypt(data, key):
    cipher = ARC4.new(key)
    return cipher.decrypt(data)

# RSA Encryption
def rsa_encrypt(data, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    return cipher_rsa.encrypt(data)

# RSA Decryption
def rsa_decrypt(data, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    return cipher_rsa.decrypt(data)

# Fernet Encryption (requires generating a Fernet key)
def fernet_encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)

# XXTEA Encryption
def xxtea_encrypt(data, key):
    return xxtea_encrypt(data, key)

# HMAC
def create_hmac(data, key):
    return HMAC.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

# PBKDF2 Key Derivation
def derive_key(password, salt):
    return PBKDF2(password.encode(), salt.encode(), dkLen=32)

# Function to chain methods (Encryption Only)
def chain_methods(data, methods, key=None, xor_key=None):
    for method in methods:
        if method == 'base64':
            data = base64_encrypt(data)
        elif method == 'zlib':
            data = zlib_encrypt(data)
        elif method == 'bzip2':
            data = bzip2_encrypt(data)
        elif method == 'gzip':
            data = gzip_encrypt(data)
        elif method == 'aes' and key:
            data = aes_encrypt(data, key.encode())
        elif method == 'blowfish' and key:
            data = blowfish_encrypt(data, key.encode())
        elif method == 'xor' and xor_key:
            data = xor_encrypt(data, xor_key)
        elif method == 'rc4' and key:
            data = rc4_encrypt(data, key.encode())
        elif method == 'rsa' and key:
            data = rsa_encrypt(data, key.encode())
        elif method == 'fernet' and key:
            data = fernet_encrypt(data, key.encode())
        elif method == 'xxtea' and key:
            data = xxtea_encrypt(data, key.encode())
        elif method == 'hmac' and key:
            data = create_hmac(data.decode(), key)
        elif method == 'pbkdf2' and key:
            salt = input("Enter a salt for PBKDF2: ")
            data = derive_key(data.decode(), salt).hex()
    return data

# Function to read file content
def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Function to write encrypted data to a file
def save_to_file(data, original_filename):
    enc_filename = f"enc_{os.path.splitext(original_filename)[0]}.py"  # Ensure .py extension
    with open(enc_filename, 'wb') as file:
        file.write(data)
    print(colored(f"🔒 Encrypted file saved as: {enc_filename}", 'green'))

def main():
    if not password_check():
        print(colored("🚨 Incorrect password. Access denied.", 'red'))
        return
    
    method_menu()
    action = input(colored("Choose action (encrypt/hash/chain): ", 'blue')).lower()
    file_path = input(colored("Enter the filename (e.g., example.py): ", 'blue'))
    
    if not os.path.exists(file_path):
        print(colored("🚨 File not found. Please try again.", 'red'))
        return
    
    data = read_file(file_path)
    
    if action == 'chain':
        methods = input(colored("Enter the methods you want to apply in order (e.g., base64,zlib,aes): ", 'blue')).lower().split(',')
        key = None
        xor_key = None
        
        if any(method in methods for method in ['aes', 'blowfish', 'rc4', 'rsa', 'fernet', 'xxtea']):
            key = input(colored("Enter the encryption key: ", 'blue'))
        
        if 'xor' in methods:
            xor_key = int(input(colored("Enter XOR key (0-255): ", 'blue')))
        
        result = chain_methods(data, methods, key, xor_key)
        save_to_file(result.encode(), os.path.basename(file_path))
    else:
        print(colored("🚨 Invalid action. Please select 'chain' for this program.", 'red'))

if __name__ == "__main__":
    main()
