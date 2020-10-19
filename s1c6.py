from base64 import b64decode
from collections import Counter
from binascii import hexlify

freq = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68,
    'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
    'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
    'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
    'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
    'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
    'j': 0.10, 'z': 0.07}

def ham_distance(txt1, txt2):
    assert len(txt1) == len(txt2)
    
    ans = 0
    for j, k in zip(txt1, txt2):
        for m in range(0, 8):
            ans += 1 if (j&2**m)^(k&2**m)!=0 else 0

    return ans

if __name__ == "__main__":
    #print(ham_distance(b'wokka wokka!!!', b'wokka wokka!!!'))


    with open("s1c6.txt", "r") as infile:
        txt = ''.join(infile.read().split('\n'))
        xor_txt = b64decode(txt)
        textlen = len(xor_txt)

        # find the most likely block size
        block_sizes = [1]*3
        smallest_hdist = [float('inf')]*3
        for i in range(2, 41):
            hdist = []
            for h in range(4):
                block1 = xor_txt[i*h:i*(h+1)]
                block2 = xor_txt[i*(h+1):i*(h+2)]

                # divide the hamming distance by the number of bits to normalize
                try:
                    hdist.append(ham_distance(block1, block2) / i)
                except AssertionError as aerr:
                    continue
            hdist = sum(hdist)/len(hdist)

            if hdist < smallest_hdist[0]:
                smallest_hdist[1:3] = smallest_hdist[0:2]
                smallest_hdist[0] = hdist
                block_sizes[1:3] = block_sizes[0:2]
                block_sizes[0] = i
            elif hdist < smallest_hdist[1]:
                smallest_hdist[2] = smallest_hdist[1]
                smallest_hdist[1] = hdist
                block_sizes[2] = block_sizes[1]
                block_sizes[1] = i
            elif hdist < smallest_hdist[2]:
                smallest_hdist[2] = hdist
                block_sizes[2] = i

        # for each block size considered likely
        for bsize in block_sizes:
            # find the single byte xor key for each of the ith elements of every block
            keys = []
            for i in range(bsize):
                # take the ith element of every block for 0 <= i <= block size
                ith_elts = xor_txt[i::bsize]

                decoded_text = ''
                xorkey = 0
                xorscore = float('inf')

                for key in range(256):
                    res = ''.join(chr(key^ch) for ch in ith_elts).lower()
                    count = Counter(res)
                    score = sum([abs(v - count[k]) for k, v in freq.items()])

                    if score < xorscore:
                        decoded_text = res
                        xorkey = key
                        xorscore = score
                        #print(decoded_text)

                keys.append(xorkey)
                #print(xorscore)

            final = ''.join(chr(ch^keys[i%bsize]) for i, ch in enumerate(xor_txt))
            print(final)
            print('\n'*5)