# Encrypts messages using Vigenère’s cipher

import sys

# check if key inputted
if not len(sys.argv) == 2:
    print("Error: wrong number of arguments, maybe you omitted the key?")
    sys.exit(1)

key = sys.argv[1]

# check if key all alphabetical
if not key.isalpha():
    print("Error: key must be all alphabetical!")
    sys.exit(1)

# prompt user for input
print("plaintext: ", end="")
plaintext = input()

# convert the key into all upper cases
key = key.upper()

print("ciphertext: ", end="")

j = 0
n = len(key)

# encrypts plaintext with key
for c in plaintext:
    if c.isupper():
        print(chr(((ord(c) - 65) + (ord(key[j % n]) - 65)) % 26 + 65), end="")
        j += 1
    elif c.islower():
        print(chr(((ord(c) - 97) + (ord(key[j % n]) - 65)) % 26 + 97), end="")
        j += 1
    else:
        print(c, end="")

print()
