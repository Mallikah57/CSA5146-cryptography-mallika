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

def find_prime_factors(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    raise ValueError("No prime factors found")

# Given values
e = 31
n = 3599

# Step 1: Factorize n
p, q = find_prime_factors(n)
print(f"Prime factors of n ({n}) are p: {p}, q: {q}")

# Step 2: Compute φ(n)
phi_n = (p - 1) * (q - 1)
print(f"φ(n) = ({p} - 1) * ({q} - 1) = {phi_n}")

# Step 3: Find the private key d
d = mod_inverse(e, phi_n)
print(f"The private key d is: {d}")
