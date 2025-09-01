# Vigenere Encryption

def vigenere_cipher(text, key):

    out = []
    keys = [ord(char.upper()) - ord('A') for char in key]
    key_index = 0

    for char in text:
        if char.isupper():
            base = ord('A')
            out.append(chr((ord(char) - base + keys[key_index]) % 26 + base))
            key_index = (key_index + 1) % len(keys)

        elif char.islower():
            base = ord('a')
            out.append(chr((ord(char) - base + keys[key_index]) % 26 + base))
            key_index = (key_index + 1) % len(keys)

        else:
            out.append(char)

    return ''.join(out)



