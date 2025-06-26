import requests
from urllib.parse import unquote
import random

# HTTP Status Codes Reference
status_codes = {
    200: "OK - Success",
    201: "Created - Request fulfilled and resource created",
    401: "Unauthorized - Authentication needed",
    403: "Forbidden - Server refuses the request",
    404: "Not Found - Resource not found",
    410: "Gone - Resource permanently removed",
    418: "I'm a teapot - Joke status code",
    420: "Enhance Your Calm - Rate limited (not official)",
    451: "Unavailable For Legal Reasons - Blocked due to law",
    500: "Internal Server Error - Generic server error"
}

print("HTTP Status Codes Reference:")
for code, meaning in status_codes.items():
    print(f"{code}: {meaning}")
print()

# Fetch Trivia Question
url = "https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986"
response = requests.get(url)

# Check HTTP Response
if response.status_code != 200:
    raise ValueError(f'API error {response.status_code}: {status_codes.get(response.status_code, "Unknown error")}')

# Parse JSON
body = response.json()
if body['response_code'] != 0:
    raise ValueError(f'OpenTDB error: {body["response_code"]}')

# Extract and Decode Question
question_data = body['results'][0]
category = unquote(question_data['category'])
difficulty = unquote(question_data['difficulty'])
question_text = unquote(question_data['question'])
correct_answer = unquote(question_data['correct_answer'])
incorrect_answers = [unquote(ans) for ans in question_data['incorrect_answers']]

# Combine and Shuffle Answers
all_answers = incorrect_answers + [correct_answer]
random.shuffle(all_answers)

# Display the Question
print(f"Category: {category}")
print(f"Difficulty: {difficulty}")
print()
print(f"{question_text}")
print()

for i, answer in enumerate(all_answers, start=1):
    print(f"{i}. {answer}")

# User Input
try:
    choice = int(input("\nEnter the number of your answer: "))
    if 1 <= choice <= len(all_answers):
        selected_answer = all_answers[choice - 1]
        if selected_answer == correct_answer:
            print("\nCorrect!")
        else:
            print(f"\nIncorrect. The correct answer was: {correct_answer}")
    else:
        print("\nInvalid choice. Number out of range.")
except ValueError:
    print("\nInvalid input. Please enter a number.")
