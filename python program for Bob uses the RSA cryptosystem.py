from Crypto.Util.number import getPrime, inverse

# RSA key generation
def generate_rsa_keys(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Commonly used prime exponent
    d = inverse(e, phi)
    return (e, n), (d, n)

# RSA encryption
def rsa_encrypt(m, pub_key):
    e, n = pub_key
    return pow(m, e, n)

# RSA decryption
def rsa_decrypt(c, priv_key):
    d, n = priv_key
    return pow(c, d, n)

# Precompute encrypted values for each possible plaintext (0 to 25)
def precompute_encryptions(pub_key):
    precomputed = {}
    for i in range(26):
        precomputed[rsa_encrypt(i, pub_key)] = i
    return precomputed

# Encrypt a message where each character is represented by an integer (0 to 25)
def encrypt_message(message, pub_key):
    encrypted_message = [rsa_encrypt(ord(char) - ord('A'), pub_key) for char in message]
    return encrypted_message

# Decrypt a message using precomputed values
def decrypt_message(encrypted_message, precomputed):
    decrypted_message = ''.join(chr(precomputed[c] + ord('A')) for c in encrypted_message)
    return decrypted_message

# Main program
bits = 1024
pub_key, priv_key = generate_rsa_keys(bits)

# Example message
message = "HELLO"

# Encrypt the message
encrypted_message = encrypt_message(message, pub_key)
print("Encrypted message:", encrypted_message)

# Precompute encryptions
precomputed = precompute_encryptions(pub_key)

# Decrypt the message using precomputed values
decrypted_message = decrypt_message(encrypted_message, precomputed)
print("Decrypted message:", decrypted_message)
