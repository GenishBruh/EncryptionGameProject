# Caesar Encryption

def caesar_cipher(text, key):
    key = key % 26
    out = []

    for char in text:
        if 'A' <= char <= 'Z':
            base = ord('A')
            out.append(chr(base + (ord(char) - base + key) % 26))
        elif 'a' <= char <= 'z':
            base = ord('a')
            out.append(chr(base + (ord(char) - base + key) % 26))
        else:
            out.append(char)

    return ''.join(out)