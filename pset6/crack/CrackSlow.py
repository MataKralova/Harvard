#!/usr/bin/env python3

# Cracks password if hashed version provided (and if hash DES-based)
# Done by Mata

import cs50
import crypt
import itertools
import string
import sys

if not len(sys.argv) == 2:
    print("Error: wrong number of arguments, maybe you forgot the hash?")
    sys.exit(1)

hash = sys.argv[1]
salts = [hash[0], hash[1]]
salt = ''.join(salts)  # creates salt from provided hash
A = ord('A')
end = ord('{')  # character following "z" in ASCII

# handles 1-character strings
for key0 in range(A, end):
    if key0 > 90 and key0 < 97:  # skips non-alpha characters
        continue
    key = chr(key0)  # creates key string
    hashed = crypt.crypt(key, salt)  # hashes key string
    if hashed == hash:  # compares hashed key with provided hash
        print(key)
        sys.exit(0)

# handles 2-character strings
for key1 in range(A, end):
    if key1 > 90 and key1 < 97:
        continue
    for key0 in range(A, end):
        if key0 > 90 and key0 < 97:
            continue
        chars = [chr(key0), chr(key1)]
        key = ''.join(chars)
        hashed = crypt.crypt(key, salt)
        if hashed == hash:
            print(key)
            sys.exit(0)

# handles 3-character strings
for key2 in range(A, end):
    if key2 > 90 and key2 < 97:
        continue
    for key1 in range(A, end):
        if key1 > 90 and key1 < 97:
            continue
        for key0 in range(A, end):
            if key0 > 90 and key0 < 97:
                continue
            chars = [chr(key0), chr(key1), chr(key2)]
            key = ''.join(chars)
            hashed = crypt.crypt(key, salt)
            if hashed == hash:
                print(key)
                sys.exit(0)

# handles 4-character strings
for key3 in range(A, end):
    if key3 > 90 and key3 < 97:
        continue
    for key2 in range(A, end):
        if key2 > 90 and key2 < 97:
            continue
        for key1 in range(A, end):
            if key1 > 90 and key1 < 97:
                continue
            for key0 in range(A, end):
                if key0 > 90 and key0 < 97:
                    continue
                chars = [chr(key0), chr(key1), chr(key2), chr(key3)]
                key = ''.join(chars)
                hashed = crypt.crypt(key, salt)
                if hashed == hash:
                    print(key)
                    sys.exit(0)

# handles 5-character strings
for k4 in range(A, end):
    if k4 > 90 and k4 < 97:
        continue
    for k3 in range(A, end):
        if k3 > 90 and k3 < 97:
            continue
        for k2 in range(A, end):
            if k2 > 90 and k2 < 97:
                continue
            for k1 in range(A, end):
                if k1 > 90 and k1 < 97:
                    continue
                for k0 in range(A, end):
                    if k0 > 90 and k0 < 97:
                        continue
                    chars = [chr(k0), chr(k1), chr(k2), chr(k3), chr(k4)]
                    key = ''.join(chars)
                    hashed = crypt.crypt(key, salt)
                    if hashed == hash:
                        print(key)
                        sys.exit(0)
