from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decrypted_text

# Main program
key = b'8bytekey'  # 8 bytes key (64 bits)
plaintext = b'Hello, DES!'

# Encrypt the plaintext
ciphertext = des_encrypt(key, plaintext)
print(f"Ciphertext (hex): {binascii.hexlify(ciphertext).decode()}")

# Decrypt the ciphertext
decrypted_text = des_decrypt(key, ciphertext)
print(f"Decrypted text: {decrypted_text.decode()}")
