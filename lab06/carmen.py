import random
from geography import countries


def random_country_name():
 
    return random.choice(list(countries.keys()))


def random_hint(country):
    match random.choice(["capital", "region", "landmark0", "landmark1", "landmark2"]):
        case "capital":
            hint = "whose capital is " + country["capital"]
        case "region":
            hint = "in " + country["region"]
        case "landmark0":
            hint = "where you can find " + country["landmarks"][0]
        case "landmark1":
            hint = "where you can find " + country["landmarks"][1]
        case "landmark2":
            hint = "where you can find " + country["landmarks"][2]
    return "Carmen is in a country " + hint


current_country_name = random_country_name()
while True:
    country = countries[current_country_name]
    print("Guess where Carmen is, or say 'hint' or 'exit'.")
    guess = input("Where are you going to look? ").strip().lower()
    if guess == current_country_name:
        print("She was here, but you missed her by one hour!")
        current_country_name = random_country_name()
    elif guess == "hint":
        print(random_hint(country))
    elif guess == "exit":
        print("Thank you for playing!")
        break
    else:
        print("Oh no, she’s not here!")