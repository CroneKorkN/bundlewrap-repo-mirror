#!/usr/bin/env python

from hashlib import sha3_256
from itertools import count
from Crypto.Cipher import ChaCha20
from math import floor, ceil

def chacha_bits(input, bit_count):
    zerobyte = (0).to_bytes(length=1, byteorder='big')
    cipher = ChaCha20.new(key=sha3_256(input).digest(), nonce=zerobyte*8)
    i = 0

    while True:
        start_bit = bit_count * i
        start_byte = start_bit // 8
        start_padding = start_bit % 8

        end_bit = bit_count * i + bit_count
        end_byte = end_bit // 8
        end_padding = 8 - (end_bit % 8)

        byte_count = end_byte - start_byte

        cipher.seek(start_byte)
        ciphertext = cipher.encrypt(zerobyte*byte_count)
        shifted_ciphertext = int.from_bytes(ciphertext, byteorder='big') >> end_padding
        
        bit_mask = int('1'*bit_count, 2)
        masked_ciphertext = shifted_ciphertext & bit_mask
        
        yield masked_ciphertext
        i += 1


def chacha_chracter(input, choices):
    get_bits = chacha_bits(input, len(choices).bit_length())
    
    while True:
        choice = next(get_bits)
        if choice < len(choices):
            yield choices[choice]


def derive_string(input, length, choices):
    get_character = chacha_chracter(input, choices)
    return ''.join(next(get_character) for i in range(length))

print(
    derive_string(b'12345', length=100, choices='abcde12345')
)
