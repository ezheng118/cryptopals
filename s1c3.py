# single byte xor cipher
from binascii import unhexlify

cipher = b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
cipher = unhexlify(cipher)

# store the best scoring strings
best = []

# loop through all possible bitstrings of size 8
# and xor with cipher
for i in range(1, 512): 
    try:
        out = bytes(bytearray(x^i for x in cipher)).decode()
    except UnicodeDecodeError:
        print('can no longer decode, quitting')
        break

    vowels = 0
    consonants = 0
    for letter in out:
        if letter in ('a', 'e', 'i', 'o', 'u'):
            vowels += 1
        else:
            consonants += 1
    
    rat = vowels / (vowels + consonants)
    if abs(rat - .33) <= .1:
        best.append(i)
        print(out, f': {i}')

# running this program fails after using keys with a large enough value 
# the key = 88 (in binary)