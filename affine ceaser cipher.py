def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("a and 26 are not coprime, choose a different a")
    
    encrypted_text = ""
    for char in text.upper():
        if char.isalpha():
            p = ord(char) - ord('A')
            c = (a * p + b) % 26
            encrypted_text += chr(c + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(ciphertext, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("a and 26 are not coprime, choose a different a")
    
    decrypted_text = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("Multiplicative inverse of a does not exist, decryption impossible")
    
    for char in ciphertext.upper():
        if char.isalpha():
            c = ord(char) - ord('A')
            p = (a_inv * (c - b)) % 26
            decrypted_text += chr(p + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text

# Example usage
a = 5
b = 8
plaintext = "AFFINE CIPHER"
ciphertext = affine_encrypt(plaintext, a, b)
decrypted_text = affine_decrypt(ciphertext, a, b)

print(f"Plaintext:  {plaintext}")
print(f"Encrypted:  {ciphertext}")
print(f"Decrypted:  {decrypted_text}")
