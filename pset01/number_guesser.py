# ----------------------------------------------------------------------
# This is the file number_guesser.py

# The intent is to give you practice writing a complete, interactive
# Python program.

# Remove the comments in this file when you have completed your program.
# You can, and should, include your own comments, but please remove the
# comments that are here now.
# ----------------------------------------------------------------------

# Things to do:

# Generate a random number between 1 and 1000.

# Ask the user to guess the number. In your prompt, let the user know they
# can type 'bye' or 'exit' to quit the program.
#
# If their guess is not made up entirely of digits, print "Please enter a valid
# number" and ask them to guess again.
#
# If the guess is too high, print "Too high!" and continue asking.
#
# If the guess is too low, print "Too low!" and continue asking.
#
# If the guess is correct, print "Congratulations! You guessed the number!" along
# with the number of attempts it took to guess the number. Start over with a new
# random number. Make sure to zero out the number of attempts.

# Please note: There are likely to be a number of Python guessing games online,
# and most GenAI systems can probably write this for you. Don’t rely on them,
# as they rob you of a chance to practice your Python skills and they might not
# even be correct. Perhaps, worse, they might not follow the instructions
# exactly as given.

import random

print("Welcome to the Number Guesser!")
print("Guess a number between 1 and 1000.")
print("Type 'bye' or 'exit' to quit.\n")

while True:
    number = random.randint(1, 1000)
    attempts = 0

    while True:
        guess = input("Enter your guess: ")

        if guess.lower() == 'bye' or guess.lower() == 'exit':
            print("Thanks for playing! Goodbye.")
            exit()

        if not guess.isdigit():
            print("Please enter a valid number")
            continue

        guess_num = int(guess)
        attempts += 1

        if guess_num > number:
            print("Too high!")
        elif guess_num < number:
            print("Too low!")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts!\n")
            break
