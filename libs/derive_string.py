#!/usr/bin/env python

from hashlib import sha3_256
from itertools import count, islice
from Crypto.Cipher import ChaCha20
from math import floor, ceil
from time import sleep
from os import environ
from sys import stderr

def debug(*args):
    if 'DEBUG' in environ:
        print(*args, file=stderr)

def chacha_bits(input, bit_count):
    zerobyte = (0).to_bytes(length=1, byteorder='big')
    cipher = ChaCha20.new(key=sha3_256(input).digest(), nonce=zerobyte*8)
    i = 0

    while True:
        debug(f'--- BITS {i} ---')
        start_bit = bit_count * i
        start_byte = start_bit // 8
        start_padding = start_bit % 8
        debug('start_bit', start_bit)
        debug('start_byte', start_byte)
        debug('start_padding', start_padding)

        end_bit = bit_count * i + bit_count
        end_byte = end_bit // 8
        end_padding = 8 - (end_bit % 8)
        debug('end_bit', end_bit)
        debug('end_byte', end_byte)
        debug('end_padding', end_padding)
        
        byte_count = (end_byte - start_byte) + 1
        debug('byte_count', byte_count)

        cipher.seek(start_byte)
        cipherint = int.from_bytes(cipher.encrypt(zerobyte*byte_count), byteorder='big')
        debug('ciphertext', bin(cipherint))
        shifted_cipherint = cipherint >> end_padding
        debug('shifted_ciphertext', bin(shifted_cipherint))
        
        bit_mask = int('1'*bit_count, 2)
        debug('bit_mask', bin(bit_mask))
        masked_cipherint = shifted_cipherint & bit_mask
        debug('masked_ciphertext', bin(masked_cipherint))

        debug('')
        yield masked_cipherint
        i += 1


def chacha_chracter(input, choices):
    get_bits = chacha_bits(input, len(choices).bit_length())
    
    while True:
        key = next(get_bits)
        if key < len(choices):
            yield choices[key]


def derive_string(input, length, choices):
    get_character = chacha_chracter(input, choices)
    return bytes(islice(get_character, length))

print(
    derive_string(b'12344', length=100, choices=b'abcdefghijklmnopqrstuvwxyz0123456789')
)
