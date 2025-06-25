import random

# list of templates with text and author
templates = [
    {"text": "the :adjective :animal likes to :verb near the :place.", "author": "alex"},
    {"text": "i saw a :color :object that could :verb faster than a :animal.", "author": "jack"},
    {"text": "never trust a :adjective :profession who owns a :color :vehicle.", "author": "mia"},
    {"text": "on my way to :place, i found a :adjective :thing eating a :food.", "author": "sara"},
    {"text": "the :animal wore a :color hat while trying to :verb a :object.", "author": "liam"},
    {"text": "once upon a time, a :adjective :animal learned to :verb perfectly.", "author": "noah"},
    {"text": "the :profession was shocked when the :adjective :object started to :verb.", "author": "emma"},
    {"text": "yesterday i met a :adjective :person who gave me a :color :item.", "author": "olivia"},
    {"text": "the :adjective :vehicle flew over the :place while dropping :plural_noun.", "author": "ava"},
    {"text": "beware of the :adjective :creature that likes to :verb during the :time.", "author": "lucas"},
]

# set of yes answers
yes_answers = {"yes", "y", "yeah", "yep", "sí", "oui", "sure", "ok", "okay"}

# loop for the game
while True:
    template = random.choice(templates)
    text = template["text"]
    author = template["author"]

    # find placeholders starting with :
    words = text.split()
    prompts = [word[1:] for word in words if word.startswith(":")]

    # make unique prompts
    prompts = list(set(prompts))

    # ask user for each prompt
    answers = {}
    for prompt in prompts:
        while True:
            user_input = input(f"enter a {prompt}: ").strip()
            if 1 <= len(user_input) <= 30:
                answers[prompt] = user_input
                break
            else:
                print("input must be between 1 and 30 characters.")

    # replace placeholders with answers
    result = []
    for word in words:
        if word.startswith(":"):
            result.append(answers[word[1:]])
        else:
            result.append(word)
    sentence = " ".join(result)

    print()
    print(sentence)
    print()
    print(f"(template by {author})")
    print()

    # ask to play again
    play_again = input("play again? ").strip().lower()
    if play_again not in yes_answers:
        print("thanks for playing!")
        break
