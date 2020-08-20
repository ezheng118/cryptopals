# fixed xor
from binascii import unhexlify, hexlify

# here a is the encoded input and 
# b functions as the key used for decoding
a = unhexlify(b'1c0111001f010100061a024b53535009181c')
b = unhexlify(b'686974207468652062756c6c277320657965')

out = bytes(bytearray(x^y for x,y in zip(a,b)))

print(out)

out = hexlify(out)

if out == b'746865206b696420646f6e277420706c6179':
    print('xor success')