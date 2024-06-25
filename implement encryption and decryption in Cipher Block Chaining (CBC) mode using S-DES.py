def permute(block, table):
    return [block[i] for i in table]

def left_shift(bits, shift_count):
    return bits[shift_count:] + bits[:shift_count]

def generate_subkeys(key):
    # P10 permutation
    P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    key = permute(key, P10)

    # Split into left and right halves
    left, right = key[:5], key[5:]

    # Left shifts
    left = left_shift(left, 1)
    right = left_shift(right, 1)

    # P8 permutation to get K1
    P8 = [5, 2, 6, 3, 7, 4, 9, 8]
    K1 = permute(left + right, P8)

    # Left shifts
    left = left_shift(left, 2)
    right = left_shift(right, 2)

    # P8 permutation to get K2
    K2 = permute(left + right, P8)

    return K1, K2

def sbox(input, sbox):
    row = int(f"{input[0]}{input[3]}", 2)
    col = int(f"{input[1]}{input[2]}", 2)
    return [int(x) for x in format(sbox[row][col], '02b')]

def f_k(bits, key):
    # Expand and permute
    EP = [3, 0, 1, 2, 1, 2, 3, 0]
    expanded = permute(bits[4:] + bits[:4], EP)

    # XOR with key
    xor_result = [expanded[i] ^ key[i] for i in range(8)]

    # S-boxes
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]
    left, right = xor_result[:4], xor_result[4:]
    sbox_output = sbox(left, S0) + sbox(right, S1)

    # P4 permutation
    P4 = [1, 3, 2, 0]
    p4_output = permute(sbox_output, P4)

    # XOR with left half of the original bits
    left_original = bits[:4]
    right_original = bits[4:]
    result = [left_original[i] ^ p4_output[i] for i in range(4)]

    return result + right_original

def sdes_encrypt(plaintext, K1, K2):
    # Initial permutation
    IP = [1, 5, 2, 0, 3, 7, 4, 6]
    initial_permutation = permute(plaintext, IP)

    # Apply fk with K1
    left_half = initial_permutation[:4]
    right_half = initial_permutation[4:]
    first_fk_result = f_k(initial_permutation, K1)

    # Swap halves
    swapped = first_fk_result[4:] + first_fk_result[:4]

    # Apply fk with K2
    final_fk_result = f_k(swapped, K2)

    # Inverse initial permutation
    IP_inv = [3, 0, 2, 4, 6, 1, 7, 5]
    ciphertext = permute(final_fk_result, IP_inv)

    return ciphertext

def sdes_decrypt(ciphertext, K1, K2):
    # Initial permutation
    IP = [1, 5, 2, 0, 3, 7, 4, 6]
    initial_permutation = permute(ciphertext, IP)

    # Apply fk with K2
    left_half = initial_permutation[:4]
    right_half = initial_permutation[4:]
    first_fk_result = f_k(initial_permutation, K2)

    # Swap halves
    swapped = first_fk_result[4:] + first_fk_result[:4]

    # Apply fk with K1
    final_fk_result = f_k(swapped, K1)

    # Inverse initial permutation
    IP_inv = [3, 0, 2, 4, 6, 1, 7, 5]
    plaintext = permute(final_fk_result, IP_inv)

    return plaintext

def xor_bits(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def encrypt_cbc(plaintext, key, iv):
    K1, K2 = generate_subkeys(key)
    ciphertext = []
    previous_block = iv

    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        block = xor_bits(block, previous_block)
        encrypted_block = sdes_encrypt(block, K1, K2)
        ciphertext.extend(encrypted_block)
        previous_block = encrypted_block

    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    K1, K2 = generate_subkeys(key)
    plaintext = []
    previous_block = iv

    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_block = sdes_decrypt(block, K1, K2)
        decrypted_block = xor_bits(decrypted_block, previous_block)
        plaintext.extend(decrypted_block)
        previous_block = block

    return plaintext

# Example usage
plaintext = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]
key = [0, 1, 1, 1, 1, 1, 1, 0, 1]
iv = [1, 0, 1, 0, 1, 0, 1, 0]

ciphertext = encrypt_cbc(plaintext, key, iv)
decrypted_plaintext = decrypt_cbc(ciphertext, key, iv)

print("Plaintext:         ", ''.join(map(str, plaintext)))
print("Ciphertext:        ", ''.join(map(str, ciphertext)))
print("Decrypted Plaintext:", ''.join(map(str, decrypted_plaintext)))
