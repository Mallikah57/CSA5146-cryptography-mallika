def create_playfair_matrix(key):
    key = "".join(sorted(set(key), key=key.index)).replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = key + ''.join([ch for ch in alphabet if ch not in key])
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, letter):
    for i, row in enumerate(matrix):
        if letter in row:
            return (i, row.index(letter))
    return None

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

# Create the Playfair matrix with the provided key
key = "PLAYFAIREXAMPLE"
matrix = create_playfair_matrix(key)

# The ciphertext received
ciphertext = ("KXJEY UREBE ZWEHE WRYTU HEYFS "
              "KREHE GOYFI WTTTU OLKSY CAJPO "
              "BOTEI ZONTX BYBNT GONEY CUZWR "
              "GDSON SXBOU YWRHE BAAHY USEDQ").replace(" ", "")

# Decrypt the ciphertext
decrypted_text = playfair_decrypt(ciphertext, matrix)

print("Playfair Matrix:")
for row in matrix:
    print(row)

print("\nCiphertext:", ciphertext)
print("Decrypted Text:", decrypted_text)
