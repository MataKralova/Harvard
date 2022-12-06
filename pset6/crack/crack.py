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

# handles 1-character strings (source: https://stackoverflow.com \
# /questions/41092474/how-to-get-itertool-product-to-generate-strings- \
# instead-of-list-of-chars-and-the?rq=1)
for item in itertools.product(string.ascii_letters, repeat=1):
    key = ''.join(list(item))
    hashed = crypt.crypt(key, salt)
    if hashed == hash:
        print(key)
        sys.exit(0)

# handles 2-character strings
for item in itertools.product(string.ascii_letters, repeat=2):
    key = ''.join(list(item))
    hashed = crypt.crypt(key, salt)
    if hashed == hash:
        print(key)
        sys.exit(0)

# handles 3-character strings
for item in itertools.product(string.ascii_letters, repeat=3):
    key = ''.join(list(item))
    hashed = crypt.crypt(key, salt)
    if hashed == hash:
        print(key)
        sys.exit(0)

# handles 4-character strings
for item in itertools.product(string.ascii_letters, repeat=4):
    key = ''.join(list(item))
    hashed = crypt.crypt(key, salt)
    if hashed == hash:
        print(key)
        sys.exit(0)

# handles 5-character strings
for item in itertools.product(string.ascii_letters, repeat=5):
    key = ''.join(list(item))
    hashed = crypt.crypt(key, salt)
    if hashed == hash:
        print(key)
        sys.exit(0)
