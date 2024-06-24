def create_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = "".join(sorted(set(key), key=key.index)).replace("J", "")
    matrix = key + ''.join([ch for ch in alphabet if ch not in key])
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, letter):
    for i, row in enumerate(matrix):
        if letter in row:
            return (i, row.index(letter))
    return None

def prepare_text(plaintext):
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    prepared_text = ""
    i = 0
    while i < len(plaintext):
        prepared_text += plaintext[i]
        if i + 1 < len(plaintext) and plaintext[i] == plaintext[i + 1]:
            prepared_text += 'X'
        elif i + 1 < len(plaintext):
            prepared_text += plaintext[i + 1]
        else:
            prepared_text += 'X'
        i += 2
    return prepared_text

def playfair_encrypt(plaintext, matrix):
    plaintext = prepare_text(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        row1, col1 = find_position(matrix, plaintext[i])
        row2, col2 = find_position(matrix, plaintext[i + 1])
        
        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2] + matrix[row2][col1]
    return ciphertext

def playfair_decrypt(ciphertext, matrix):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        row1, col1 = find_position(matrix, ciphertext[i])
        row2, col2 = find_position(matrix, ciphertext[i + 1])
        
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]
    return plaintext

# Create the Playfair matrix with the given key
key = "MFHIJKUNOPQZVWXELARGDSTBC"
matrix = create_playfair_matrix(key)

# Message to encrypt
plaintext = "Must see you over Cadogan West. Coming at once."
ciphertext = playfair_encrypt(plaintext, matrix)
decrypted_text = playfair_decrypt(ciphertext, matrix)

print("Playfair Matrix:")
for row in matrix:
    print(row)
print("\nPlaintext: ", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted Text:", decrypted_text)
