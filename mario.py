# Prints a double pyramid as if from the Mario game

# Ask user for input
while True:
    print("Choose height of the pyramid (max 23): ", end="")
    h = int(input())
    if h > -1 and h < 24:
        break

# Treat zero
if h == 0:
    exit

# Print pyramid
for r in range(h, 0, -1):  # prints rows
    print(" " * (r - 1), end="")  # prints spaces
    print("#" * (h + 1 - r), end="")  # prints left-half bricks
    print("  ", end="")
    print("#" * (h + 1 - r), end="")  # prints right-half bricks
    print()  # prints final new line
