from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# Define block size for DES
BLOCK_SIZE = 8

def pad(plaintext):
    padding_length = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    padding = bytes([0] * (padding_length - 1)) + bytes([1])
    return plaintext + padding

def unpad(plaintext):
    return plaintext.rstrip(b'\x00').rstrip(b'\x01')

def encrypt_ecb(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_plaintext = pad(plaintext)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def decrypt_ecb(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext)
    return plaintext

def encrypt_cbc(plaintext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext)
    return plaintext

def encrypt_cfb(plaintext, key, iv):
    cipher = DES.new(key, DES.MODE_CFB, iv, segment_size=8)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def decrypt_cfb(ciphertext, key, iv):
    cipher = DES.new(key, DES.MODE_CFB, iv, segment_size=8)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Example usage
key = get_random_bytes(8)
iv = get_random_bytes(8)

plaintext = b"Hello, DES encryption!"

# ECB mode
ciphertext_ecb = encrypt_ecb(plaintext, key)
decrypted_ecb = decrypt_ecb(ciphertext_ecb, key)
print("ECB mode:")
print("Ciphertext:", ciphertext_ecb)
print("Decrypted:", decrypted_ecb)

# CBC mode
ciphertext_cbc = encrypt_cbc(plaintext, key, iv)
decrypted_cbc = decrypt_cbc(ciphertext_cbc, key, iv)
print("\nCBC mode:")
print("Ciphertext:", ciphertext_cbc)
print("Decrypted:", decrypted_cbc)

# CFB mode
ciphertext_cfb = encrypt_cfb(plaintext, key, iv)
decrypted_cfb = decrypt_cfb(ciphertext_cfb, key, iv)
print("\nCFB mode:")
print("Ciphertext:", ciphertext_cfb)
print("Decrypted:", decrypted_cfb)
