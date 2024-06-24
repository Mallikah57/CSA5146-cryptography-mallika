#include <stdio.h>
#include <string.h>

#define MAX_CHARS 256

// Function to count the frequency of each character
void count_frequency(const char *ciphertext, int *freq) {
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        if (ciphertext[i] != ' ' && ciphertext[i] != '\n') {
            freq[(unsigned char)ciphertext[i]]++;
        }
    }
}

// Function to print the frequency of each character
void print_frequency(const int *freq) {
    for (int i = 0; i < MAX_CHARS; i++) {
        if (freq[i] > 0) {
            printf("Character '%c' has frequency %d\n", i, freq[i]);
        }
    }
}

// Function to perform substitution based on provided key
void decrypt(const char *ciphertext, const char *key) {
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        if (ciphertext[i] != ' ' && ciphertext[i] != '\n') {
            putchar(key[(unsigned char)ciphertext[i]]);
        } else {
            putchar(ciphertext[i]);
        }
    }
    putchar('\n');
}

int main() {
    const char *ciphertext = "53‡‡†305))6*;4826)4‡.)4‡);806*;48†8¶60))85;;]8*;:‡*8†83\n"
                             "(88)5*†;46(;88*96*?;8)*‡(;485);5*†2:*‡(;4956*2(5*—4)8¶8*\n"
                             ";4069285);)6†8)4‡‡;1(‡9;48081;8:8‡1;48†85;4)485†528806*81 (‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?;\n";
    
    int freq[MAX_CHARS] = {0};
    count_frequency(ciphertext, freq);
    print_frequency(freq);

    // Hypothetical key based on frequency analysis and common patterns
    char key[MAX_CHARS];
    memset(key, 0, sizeof(key));
    
    // Initialize key with common mappings (this would normally be determined through analysis)
    key['‡'] = 'e';
    key[')'] = 't';
    key[';'] = 'h';
    key['†'] = 'a';
    key['5'] = 'o';
    key['4'] = 'i';
    key['8'] = 's';
    key['6'] = 'n';
    key['*'] = 'r';
    key['3'] = 'm';
    key['0'] = 'u';
    key['9'] = 'd';
    key['1'] = 'w';
    key[':'] = 'y';
    key['('] = 'l';
    key['¶'] = 'f';
    key[']'] = 'c';
    key['?'] = 'b';
    key['—'] = 'g';

    printf("\nDecrypted message:\n");
    decrypt(ciphertext, key);

    return 0;
}
