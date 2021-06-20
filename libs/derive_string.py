#!/usr/bin/env python

from hashlib import sha3_256
from itertools import count
from Crypto.Cipher import ChaCha20
from math import ceil

def derive_string(input, length, choices):
    result = ""
    cipher = ChaCha20.new(key=sha3_256(input).digest())
    
    print(len(choices))
    
    for pow in count():
        if 2**pow > len(choices):
            break
    
    print(pow)

    while len(result) < length:
        seek = int.from_bytes(cipher.encrypt(b'0'*ceil(pow/8)), byteorder='little')
        print(seek, len(choices))
        if seek < len(choices):
            result += choices[seek]
        else:
            continue

    return result

print(
    derive_string(b'12345', length=100, choices='abcde12345')
)
