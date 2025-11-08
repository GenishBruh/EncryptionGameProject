import random
import string


DIFFICULTY_INFO = {
    "Caesar Easy": (
        "Caesar Easy:\n"
        "- Word length: 4–6 characters\n"
        "- Key range: 1–3\n"
        "- Time limit: 60 seconds"
    ),
    "Caesar Medium": (
        "Caesar Medium:\n"
        "- Word length: 6–10 characters\n"
        "- Key range: 4-7\n"
        "- Time limit: 45 seconds"
    ),
    "Caesar Hard": (
        "Caesar Hard:\n"
        "- Word length: 10–15 characters\n"
        "- Key range: 8-12\n"
        "- Time limit: 30 seconds"
    ),
    "Vigenere Easy": (
        "Vigenere Easy:\n"
        "- Word length: 4–6 characters\n"
        "- Key length: 1-2 letters\n"
        "- Key range: A-C\n"
        "- Time limit: 90 seconds"
    ),
    "Vigenere Medium": (
        "Vigenere Medium:\n"
        "- Word length: 6–10 characters\n"
        "- Key length: 2-3 letters\n"
        "- Key range: D-F\n"
        "- Time limit: 60 seconds"
    ),
    "Vigenere Hard": (
        "Vigenere Hard:\n"
        "- Word length: 10–15 characters\n"
        "- Key length: 3-4 letters\n"
        "- Key range: G-K\n"
        "- Time limit: 45 seconds"
    ),
    "Zigzag Easy": (
        "Zigzag Easy:\n"
        "- Word length: 4-6 characters\n"
        "- Number of rails: 2\n"
        "- Time limit: 90 seconds"
    ),
    "Zigzag Medium": (
        "Zigzag Medium:\n"
        "- Word length: 6-10 characters\n"
        "- Number of rails: 3–4\n"
        "- Time limit: 60 seconds"
    ),
    "Zigzag Hard": (
        "Zigzag Hard:\n"
        "- Word length: 10-15 characters\n"
        "- Number of rails: 4–5\n"
        "- Time limit: 45 seconds"
    ),
}

ENCRYPTION_INFO = {
    "caesar": ("Each letter in the message gets shifted a number of places in the alphabet, depending on the key.\n"
                "For example:\n\n"
                "Key : 2  |  ABC → CDE\n"
                "A → C | B → D | C → E\n"
                "Your task is to reverse the encryption."),
    "vigenere": ("Each letter in the message is shifted according to the corresponding letter in the keyword.\n"
            "The keyword repeats to match the length of the message.\n"
            "For example:\n\n"
            "Keyword : ABC | Word to encrypt : Hello\n"
            "(A shifts by 1, B shifts by 2, etc.)\n\n"
            "H → I | e → g | l → o | l → m | o → q\n"
            "Hello → Igomq"),
    "zigzag": ("The message is written in a zigzag pattern across a set number of rows (rails).\n"
            "It is then read row by row to create the encrypted text.\n"
            "For example, with 3 rails:\n\n"
            "M . . . A . .\n"
            ". E . S . G .\n"
            ". . S . . . E\n"
            "MESSAGE → MAESGSE\n"
            "Your task is to reconstruct the zigzag to reveal the original message.")
}
# Load the words once
with open("google-10000-english-no-swears.txt", "r") as file:
    words = [line.strip() for line in file]

words1 = [w for w in words if 4 <= len(w) <= 6]
words2 = [w for w in words if 6 <= len(w) <= 10]
words3 = [w for w in words if 10 <= len(w) <= 15]

def rand_short_word():
    return random.choice(words1)

def rand_regular_word():
    return random.choice(words2)

def rand_long_word():
    return random.choice(words3)


GAME_CONFIG = {
            # Caesar
            "easy_caesar": {
                "timer_counts": 60,
                "word": rand_short_word,
                "key_range": (1, 3),
                "encryption_func": "caesar",
                "score_given" : 10
            },
            "medium_caesar": {
                "timer_counts": 45,
                "word": rand_regular_word,
                "key_range": (4, 7),
                "encryption_func": "caesar",
                "score_given": 25
            },
            "hard_caesar": {
                "timer_counts": 30,
                "word": rand_long_word,
                "key_range": (8, 12),
                "encryption_func": "caesar",
                "score_given": 50
            },

            # Vigenère
            "easy_vigenere": {
                "timer_counts": 90,
                "word": rand_short_word,
                "key_length": 2,
                "key_range": ("A", "C"),
                "encryption_func": "vigenere",
                "score_given": 30
            },
            "medium_vigenere": {
                "timer_counts": 60,
                "word": rand_regular_word,
                "key_length": 3,
                "key_range": ("D", "F"),
                "encryption_func": "vigenere",
                "score_given": 60
            },
            "hard_vigenere": {
                "timer_counts": 45,
                "word": rand_long_word,
                "key_length": 4,
                "key_range": ("G", "K"),
                "encryption_func": "vigenere",
                "score_given": 100
            },

            # Zigzag
            "easy_zigzag": {
                "timer_counts": 90,
                "word": rand_short_word,
                "rails": 2,
                "encryption_func": "zigzag",
                "score_given": 50
            },
            "medium_zigzag": {
                "timer_counts": 60,
                "word": rand_regular_word,
                "rails": 3,
                "encryption_func": "zigzag",
                "score_given": 110
            },
            "hard_zigzag": {
                "timer_counts": 45,
                "word": rand_long_word,
                "rails": 4,
                "encryption_func": "zigzag",
                "score_given": 200
            }
        }

