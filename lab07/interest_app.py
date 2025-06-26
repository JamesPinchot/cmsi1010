import locale
from interest import investment_value, years_to_reach_goal

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # use your appropriate locale


def ask_float(prompt):
    return float(input(prompt))


def ask_int(prompt):
    return int(input(prompt))


def main():
    print("welcome to the interest app!")

    while True:
        print("\nwhat would you like to do?")
        print("1: calculate future balance")
        print("2: calculate years to reach a goal")
        print("3: exit")
        choice = input("enter 1, 2, or 3: ")

        if choice == '1':
            start = ask_float("starting balance: ")
            rate = ask_float("interest rate (e.g., 0.05 for 5%): ")
            tax = ask_float("tax rate on interest (e.g., 0.25 for 25%): ")
            deposit = ask_float("yearly deposit: ")
            years = ask_int("number of years: ")

            result = investment_value(start, rate, tax, deposit, years)
            print(f"after {years} years, you will have {locale.currency(result, grouping=True)}")

        elif choice == '2':
            start = ask_float("starting balance: ")
            rate = ask_float("interest rate (e.g., 0.05 for 5%): ")
            tax = ask_float("tax rate on interest (e.g., 0.25 for 25%): ")
            deposit = ask_float("yearly deposit: ")
            goal = ask_float("goal amount: ")

            years = years_to_reach_goal(start, rate, tax, deposit, goal)
            print(f"it will take {years} years to reach {locale.currency(goal, grouping=True)}")

        elif choice == '3':
            print("thanks for using the interest app. goodbye!")
            break
        else:
            print("invalid choice. please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
