from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import binascii

def generate_3des_key():
    """Generate a 3DES key. 3DES keys are 16 or 24 bytes long."""
    while True:
        key = get_random_bytes(24)
        try:
            DES3.adjust_key_parity(key)
            return key
        except ValueError:
            continue

def encrypt_3des_cbc(plaintext, key, iv):
    """Encrypt plaintext using 3DES in CBC mode."""
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_text = pad(plaintext, DES3.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def decrypt_3des_cbc(ciphertext, key, iv):
    """Decrypt ciphertext using 3DES in CBC mode."""
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_padded_text = cipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, DES3.block_size)
    return decrypted_text

# Main program
plaintext = b"Hello, World! This is a test message."

# Generate 3DES key and initialization vector (IV)
key = generate_3des_key()
iv = get_random_bytes(DES3.block_size)

# Encrypt the plaintext
ciphertext = encrypt_3des_cbc(plaintext, key, iv)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext).decode()}")

# Decrypt the ciphertext
decrypted_text = decrypt_3des_cbc(ciphertext, key, iv)
print(f"Decrypted text: {decrypted_text.decode()}")
