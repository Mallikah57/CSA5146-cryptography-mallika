from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# S-DES parameters
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

def permute(bits, table):
    return bitarray([bits[i - 1] for i in table])

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]
    left, right = left_shift(left, 1), left_shift(right, 1)
    k1 = permute(left + right, P8)
    left, right = left_shift(left, 2), left_shift(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def sbox(input, sbox):
    row = 2 * input[0] + input[3]
    col = 2 * input[1] + input[2]
    return int2ba(sbox[row][col], length=2)

def fk(bits, subkey):
    left, right = bits[:4], bits[4:]
    expanded = permute(right, EP)
    xor_result = expanded ^ subkey
    left_half = sbox(xor_result[:4], S0)
    right_half = sbox(xor_result[4:], S1)
    p4_result = permute(left_half + right_half, P4)
    return left ^ p4_result + right

def sdes_encrypt(plaintext, subkeys):
    bits = permute(plaintext, IP)
    bits = fk(bits, subkeys[0])
    bits = bits[4:] + bits[:4]
    bits = fk(bits, subkeys[1])
    return permute(bits, IP_INV)

def sdes_decrypt(ciphertext, subkeys):
    bits = permute(ciphertext, IP)
    bits = fk(bits, subkeys[1])
    bits = bits[4:] + bits[:4]
    bits = fk(bits, subkeys[0])
    return permute(bits, IP_INV)

def cbc_encrypt(plaintext, key, iv):
    subkeys = generate_subkeys(key)
    ciphertext = bitarray()
    previous_block = iv

    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8] ^ previous_block
        encrypted_block = sdes_encrypt(block, subkeys)
        ciphertext.extend(encrypted_block)
        previous_block = encrypted_block

    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    subkeys = generate_subkeys(key)
    plaintext = bitarray()
    previous_block = iv

    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_block = sdes_decrypt(block, subkeys)
        plaintext_block = decrypted_block ^ previous_block
        plaintext.extend(plaintext_block)
        previous_block = block

    return plaintext

# Test data
iv = bitarray('10101010')
plaintext = bitarray('0000000100100011')
key = bitarray('0111111101')
expected_ciphertext = bitarray('1111010000001011')

# Encrypt the plaintext
ciphertext = cbc_encrypt(plaintext, key, iv)
print(f"Ciphertext (binary): {ciphertext.to01()}")
assert ciphertext == expected_ciphertext, "Encryption failed!"

# Decrypt the ciphertext
decrypted_plaintext = cbc_decrypt(ciphertext, key, iv)
print(f"Decrypted plaintext (binary): {decrypted_plaintext.to01()}")
assert decrypted_plaintext == plaintext, "Decryption failed!"
s
