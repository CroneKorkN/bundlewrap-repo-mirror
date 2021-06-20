#!/usr/bin/env python

from hashlib import sha3_256
from itertools import count
from Crypto.Cipher import ChaCha20
from math import floor, ceil
from time import sleep

def chacha_bits(input, bit_count):
    zerobyte = (0).to_bytes(length=1, byteorder='big')
    cipher = ChaCha20.new(key=sha3_256(input).digest(), nonce=zerobyte*8)
    i = 0

    while True:
        print('-----------------------------')
        start_bit = bit_count * i
        start_byte = start_bit // 8
        start_padding = start_bit % 8
        print('start_bit', start_bit)
        print('start_byte', start_byte)
        print('start_padding', start_padding)

        end_bit = bit_count * i + bit_count
        end_byte = end_bit // 8
        end_padding = 8 - (end_bit % 8)
        print('end_bit', end_bit)
        print('end_byte', end_byte)
        print('end_padding', end_padding)
        
        byte_count = (end_byte - start_byte) + 1
        print('byte_count', byte_count)

        cipher.seek(start_byte)
        ciphertext = cipher.encrypt(zerobyte*byte_count)
        print('ciphertext', bin(int.from_bytes(ciphertext, byteorder='big')))
        shifted_ciphertext = int.from_bytes(ciphertext, byteorder='big') >> end_padding
        print('shifted_ciphertext', bin(shifted_ciphertext))
        
        bit_mask = int('1'*bit_count, 2)
        print('bit_mask', bin(bit_mask))
        masked_ciphertext = shifted_ciphertext & bit_mask
        print('masked_ciphertext', bin(masked_ciphertext))

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
    derive_string(b'12345', length=100, choices='abcdefghijklmnopqrstuvwxyz0123456789')
)
