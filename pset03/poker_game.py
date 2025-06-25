from cards import deal, poker_classification

# loop until user types bye or exit
while True:
    user_input = input("enter the number of players(2-10): ").strip().lower()

    if user_input in ("bye", "exit"):
        break

    # check if input is a number
    if not user_input.isdigit():
        print("invalid input. please enter a number between 2 and 10.")
        continue

    num_players = int(user_input)

    # check if number is between 2 and 10
    if num_players < 2 or num_players > 10:
        print("invalid number of players. must be between 2 and 10.")
        continue

    # deal hands and print results
    hands = deal(num_players, 5)

    for hand in hands:
        hand_str = ' '.join(str(card) for card in sorted(hand, key=lambda c: (c.suit, c.rank)))
        classification = poker_classification(hand)
        print(f"{hand_str} is a {classification}")
