from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_mac(key, message, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(message)
    return ciphertext[-16:]  # The MAC is the last block of ciphertext

# Main program
# Generate a random 16-byte AES key
key = get_random_bytes(16)

# Initialization vector (IV) for CBC mode (usually 16 bytes for AES)
iv = get_random_bytes(16)

# One-block message X (16 bytes for AES)
message_x = b'YELLOW SUBMARINE'

# Compute the CBC-MAC for the one-block message X
mac_x = cbc_mac(key, message_x, iv)
print(f"CBC-MAC for one-block message X: {binascii.hexlify(mac_x).decode()}")

# Compute the two-block message X || (X ⊕ T)
block_size = 16
message_xor_mac = xor_bytes(message_x, mac_x)
two_block_message = message_x + message_xor_mac

# Compute the CBC-MAC for the two-block message X || (X ⊕ T)
mac_two_block = cbc_mac(key, two_block_message, iv)
print(f"CBC-MAC for two-block message X || (X ⊕ T): {binascii.hexlify(mac_two_block).decode()}")
