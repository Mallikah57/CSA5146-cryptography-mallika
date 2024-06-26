from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

# Constants for DES key scheduling
PC1_LEFT = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36]
PC1_RIGHT = [63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2_LEFT = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2]
PC2_RIGHT = [41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def permute(key, table):
    return ''.join([key[i - 1] for i in table])

def shift_left(key, shifts):
    return key[shifts:] + key[:shifts]

def generate_subkeys(initial_key):
    key = bin(int(binascii.hexlify(initial_key), 16))[2:].zfill(64)
    left_half = permute(key, PC1_LEFT)
    right_half = permute(key, PC1_RIGHT)

    subkeys = []
    for shift in SHIFT_SCHEDULE:
        left_half = shift_left(left_half, shift)
        right_half = shift_left(right_half, shift)
        left_subkey = permute(left_half, PC2_LEFT)
        right_subkey = permute(right_half, PC2_RIGHT)
        subkeys.append(left_subkey + right_subkey)
    return [bitstring_to_bytes(subkey) for subkey in subkeys]

# DES encryption and decryption functions
def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext, DES.block_size)
    return cipher.encrypt(padded_text)

def des_decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decrypted_text

# Main program
initial_key = b'12345678'  # 8 bytes key for DES
plaintext = b"Hello, World!"

# Generate subkeys
subkeys = generate_subkeys(initial_key)

# Encrypt the plaintext
ciphertext = des_encrypt(plaintext, initial_key)
print(f"Ciphertext: {binascii.hexlify(ciphertext).decode()}")

# Decrypt the ciphertext
decrypted_text = des_decrypt(ciphertext, initial_key)
print(f"Decrypted text: {decrypted_text.decode()}")
