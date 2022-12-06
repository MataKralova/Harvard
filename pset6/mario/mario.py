#!/usr/bin/env python3

# Prints a double pyramid as if from the Mario game
# Done by Mata

import cs50

while True:
    print("Height: ", end="")
    h = cs50.get_int()
    if h > -1 and h < 24:
        break

if h == 0:
    exit

for r in range(h, 0, -1):  # prints rows
    print(" " * (r - 1), end="")  # prints spaces
    print("#" * (h + 1 - r), end="")  # prints left-half bricks
    print("  ", end="")
    print("#" * (h + 1 - r), end="")  # prints right-half bricks
    print()  # prints final new line