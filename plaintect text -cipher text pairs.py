import numpy as np
from sympy import Matrix

def mod_inverse(matrix, modulus):
    """Compute the modular inverse of a matrix."""
    return Matrix(matrix).inv_mod(modulus)

def encrypt(plaintext, key_matrix, modulus):
    """Encrypt the plaintext using the Hill cipher with the given key matrix and modulus."""
    plaintext_vector = np.array([ord(char) - ord('A') for char in plaintext])
    ciphertext_vector = np.dot(key_matrix, plaintext_vector) % modulus
    ciphertext = ''.join(chr(int(num) + ord('A')) for num in ciphertext_vector)
    return ciphertext

def known_plaintext_attack(plaintexts, ciphertexts, modulus):
    """Recover the key matrix using known plaintext-ciphertext pairs."""
    # Create matrices from plaintext and ciphertext vectors
    P = np.array([[ord(char) - ord('A') for char in text] for text in plaintexts]).T
    C = np.array([[ord(char) - ord('A') for char in text] for text in ciphertexts]).T

    # Compute the inverse of the plaintext matrix modulo the alphabet size
    P_inv = mod_inverse(P, modulus)

    # Recover the key matrix
    key_matrix = np.dot(C, P_inv) % modulus
    return key_matrix

# Example usage
alphabet_size = 26
key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])  # Example key matrix
plaintexts = ["ACT", "CAT", "DOG"]  # Example plaintexts
ciphertexts = [encrypt(text, key_matrix, alphabet_size) for text in plaintexts]

# Perform known plaintext attack to recover the key matrix
recovered_key_matrix = known_plaintext_attack(plaintexts, ciphertexts, alphabet_size)

print("Original Key Matrix:")
print(key_matrix)
print("\nRecovered Key Matrix:")
print(recovered_key_matrix)
