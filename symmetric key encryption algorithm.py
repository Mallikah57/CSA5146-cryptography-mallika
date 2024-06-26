from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

def generate_des_key():
    """Generate a random DES key (56 bits represented as 8 bytes with the last bit of each byte used for parity)."""
    key = DES.adjust_key_parity(get_random_bytes(8))
    return key

def des_encrypt(plaintext, key):
    """Encrypt the plaintext using DES algorithm."""
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def des_decrypt(ciphertext, key):
    """Decrypt the ciphertext using DES algorithm."""
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_padded_text = cipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, DES.block_size)
    return decrypted_text

# Main program
plaintext = b"Hello, World!"  # 13 bytes plaintext, which will be padded to 16 bytes (2 blocks)

# Generate a random DES key
key = generate_des_key()
print(f"DES Key: {binascii.hexlify(key).decode()}")

# Encrypt the plaintext
ciphertext = des_encrypt(plaintext, key)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext).decode()}")

# Decrypt the ciphertext
decrypted_text = des_decrypt(ciphertext, key)
print(f"Decrypted text: {decrypted_text.decode()}")
