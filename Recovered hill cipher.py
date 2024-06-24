import numpy as np
from sympy import Matrix

class HillCipher:
    def __init__(self, key_matrix):
        self.key_matrix = np.array(key_matrix)
        self.n = self.key_matrix.shape[0]
        self.mod = 26
        self.key_matrix_inv = Matrix(self.key_matrix).inv_mod(self.mod)
        self.key_matrix_inv = np.array(self.key_matrix_inv.tolist()).astype(int)

    def encrypt(self, plaintext):
        plaintext = plaintext.upper().replace(' ', '')
        if len(plaintext) % self.n != 0:
            plaintext += 'X' * (self.n - len(plaintext) % self.n)

        plaintext_nums = [ord(char) - ord('A') for char in plaintext]
        ciphertext = ''
        
        for i in range(0, len(plaintext_nums), self.n):
            block = np.array(plaintext_nums[i:i+self.n]).reshape(-1, 1)
            encrypted_block = np.dot(self.key_matrix, block) % self.mod
            ciphertext += ''.join(chr(num[0] + ord('A')) for num in encrypted_block)
        
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.upper().replace(' ', '')
        ciphertext_nums = [ord(char) - ord('A') for char in ciphertext]
        plaintext = ''
        
        for i in range(0, len(ciphertext_nums), self.n):
            block = np.array(ciphertext_nums[i:i+self.n]).reshape(-1, 1)
            decrypted_block = np.dot(self.key_matrix_inv, block) % self.mod
            plaintext += ''.join(chr(num[0] + ord('A')) for num in decrypted_block)
        
        return plaintext

def known_plaintext_attack(plaintext_pairs, n):
    """Perform a known plaintext attack on the Hill cipher to find the key matrix."""
    plaintext_matrix = []
    ciphertext_matrix = []
    
    for plaintext, ciphertext in plaintext_pairs:
        plaintext_nums = [ord(char) - ord('A') for char in plaintext]
        ciphertext_nums = [ord(char) - ord('A') for char in ciphertext]
        
        for i in range(0, len(plaintext_nums), n):
            plaintext_block = plaintext_nums[i:i+n]
            ciphertext_block = ciphertext_nums[i:i+n]
            plaintext_matrix.append(plaintext_block)
            ciphertext_matrix.append(ciphertext_block)
    
    plaintext_matrix = Matrix(plaintext_matrix).T
    ciphertext_matrix = Matrix(ciphertext_matrix).T
    
    plaintext_matrix_inv = plaintext_matrix.inv_mod(26)
    key_matrix = (ciphertext_matrix * plaintext_matrix_inv) % 26
    key_matrix = np.array(key_matrix.tolist()).astype(int)
    
    return key_matrix

# Example usage
key = [[3, 10], [20, 9]]
hill_cipher = HillCipher(key)

# Encrypting a message
plaintext = "HELP"
ciphertext = hill_cipher.encrypt(plaintext)
print("Ciphertext:", ciphertext)

# Decrypting the message
decrypted_text = hill_cipher.decrypt(ciphertext)
print("Decrypted text:", decrypted_text)

# Known plaintext-ciphertext pairs for attack
plaintext_pairs = [("HELP", ciphertext)]

# Performing the known plaintext attack
key_matrix = known_plaintext_attack(plaintext_pairs, 2)
print("Recovered key matrix:")
print(key_matrix)

# Verifying the recovered key matrix
recovered_hill_cipher = HillCipher(key_matrix)
recovered_decrypted_text = recovered_hill_cipher.decrypt(ciphertext)
print("Decrypted text with recovered key:", recovered_decrypted_text)
