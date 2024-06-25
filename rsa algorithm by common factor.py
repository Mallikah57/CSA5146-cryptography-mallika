import math

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Given values
n = 3599  # This should be the product of two primes p and q
e = 31
plaintext_block = 527  # This is an example plaintext block that has a common factor with n

# Step 1: Find gcd of the plaintext block and n
g = gcd(plaintext_block, n)
if g > 1:
    p = g
    q = n // g
    print(f"Found factors of n: p = {p}, q = {q}")

    # Step 2: Compute φ(n)
    phi_n = (p - 1) * (q - 1)
    print(f"φ(n) = ({p} - 1) * ({q} - 1) = {phi_n}")

    # Step 3: Find the private key d
    d = mod_inverse(e, phi_n)
    print(f"The private key d is: {d}")
else:
    print("The plaintext block does not have a common factor with n.")
