

def ham_distance(text1, text2):
    ans = 0
    for i, j in zip(text1, text2):
        for k in range(0, 8):
            ans += 1 if (i&2**k)^(j&2**k)!=0 else 0

    print(ans)


text1 = b'this is a test'
text2 = b'wokka wokka!!!'