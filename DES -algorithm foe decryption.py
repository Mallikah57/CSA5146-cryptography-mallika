# Define permutation and shift tables
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

def permute(key, table):
    return [key[table[i] - 1] for i in range(len(table))]

def left_shift(key_half, num_shifts):
    return key_half[num_shifts:] + key_half[:num_shifts]

def generate_subkeys(key):
    # Initial permutation using PC1
    key_permuted = permute(key, PC1)
    # Split the key into two halves
    left_half = key_permuted[:28]
    right_half = key_permuted[28:]
    
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        # Left circular shift
        left_half = left_shift(left_half, shift)
        right_half = left_shift(right_half, shift)
        # Combine halves and apply PC2 permutation to get the subkey
        combined_key = left_half + right_half
        subkey = permute(combined_key, PC2)
        subkeys.append(subkey)
    
    return subkeys

def print_keys(keys):
    for i, key in enumerate(keys):
        key_str = ''.join(map(str, key))
        print(f"Key {i + 1}: {key_str}")

# Example usage
# 64-bit key (including 8 parity bits, typically one parity bit per byte)
# For simplicity, we will ignore the parity bits here and use a 56-bit key representation
key = [0, 0, 1, 1, 0, 0, 1, 1,
       1, 0, 0, 1, 1, 1, 0, 1,
       1, 1, 0, 0, 0, 1, 1, 1,
       1, 1, 1, 1, 0, 1, 0, 0,
       0, 0, 0, 1, 1, 1, 1, 0,
       1, 1, 1, 1, 1, 0, 0, 1,
       0, 1, 0, 0, 1, 1, 1, 0]

# Generate subkeys
subkeys = generate_subkeys(key)

# Print subkeys for encryption
print("Subkeys for Encryption:")
print_keys(subkeys)

# Reverse subkeys for decryption
subkeys_reversed = subkeys[::-1]

# Print subkeys for decryption
print("\nSubkeys for Decryption:")
print_keys(subkeys_reversed)
