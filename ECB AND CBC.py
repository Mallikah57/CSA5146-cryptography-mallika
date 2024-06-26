from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import os

# Function to simulate bit error in a bytearray
def introduce_error(data, byte_index, bit_index):
    data[byte_index] ^= (1 << bit_index)
    return data

def ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def ecb_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_padded_text = cipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, AES.block_size)
    return decrypted_text

def cbc_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_text = cipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, AES.block_size)
    return decrypted_text

# Main program
plaintext = b"THIS IS A TEST MESSAGE FOR CBC AND ECB MODES. ERROR PROPAGATION TEST."

# Generate a random AES key and IV
key = os.urandom(16)
iv = os.urandom(16)

# ECB Mode Encryption and Decryption
ciphertext_ecb = ecb_encrypt(plaintext, key)
print(f"ECB Ciphertext (hex): {binascii.hexlify(ciphertext_ecb).decode()}")

# Introduce error in ECB ciphertext
ciphertext_ecb_with_error = bytearray(ciphertext_ecb)
introduce_error(ciphertext_ecb_with_error, 1, 0)  # Introduce a bit error in the second byte
print(f"ECB Ciphertext with error (hex): {binascii.hexlify(ciphertext_ecb_with_error).decode()}")

# Decrypt ECB ciphertext with error
try:
    decrypted_ecb_with_error = ecb_decrypt(bytes(ciphertext_ecb_with_error), key)
    print(f"ECB Decrypted text with error: {decrypted_ecb_with_error.decode()}")
except Exception as e:
    print(f"ECB Decryption error: {e}")

# CBC Mode Encryption and Decryption
ciphertext_cbc = cbc_encrypt(plaintext, key, iv)
print(f"CBC Ciphertext (hex): {binascii.hexlify(ciphertext_cbc).decode()}")

# Introduce error in CBC ciphertext
ciphertext_cbc_with_error = bytearray(ciphertext_cbc)
introduce_error(ciphertext_cbc_with_error, 1, 0)  # Introduce a bit error in the second byte
print(f"CBC Ciphertext with error (hex): {binascii.hexlify(ciphertext_cbc_with_error).decode()}")

# Decrypt CBC ciphertext with error
try:
    decrypted_cbc_with_error = cbc_decrypt(bytes(ciphertext_cbc_with_error), key, iv)
    print(f"CBC Decrypted text with error: {decrypted_cbc_with_error.decode()}")
except Exception as e:
    print(f"CBC Decryption error: {e}")

