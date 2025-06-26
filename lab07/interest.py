import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # change to your locale if needed


def investment_value(start, interest_rate, tax_rate, deposit, years):
    balance = start
    for _ in range(1, years + 1):
        interest_earned = balance * interest_rate
        taxes = interest_earned * tax_rate
        balance += (interest_earned - taxes + deposit)
    return balance


def years_to_reach_goal(start, interest_rate, tax_rate, deposit, goal):
    years = 0
    balance = start
    while balance < goal:
        interest_earned = balance * interest_rate
        taxes = interest_earned * tax_rate
        balance += (interest_earned - taxes + deposit)
        years += 1
    return years


# sample test cases
if __name__ == "__main__":
    print(locale.currency(investment_value(1000, 0.05, 0, 0, 10), grouping=True))  # $1,628.89
    print(locale.currency(investment_value(1000, 0.05, 0, 100, 10), grouping=True))  # $2,886.68
    print(locale.currency(investment_value(10000, 0.13, 0.25, 1000, 30), grouping=True))  # $319,883.75
    print(locale.currency(investment_value(1, 1, 0, 0, 20), grouping=True))  # $1,048,576.00

    print("years to reach $50,000 from $1,000 with 5% interest and $100 deposit per year:",
          years_to_reach_goal(1000, 0.05, 0, 100, 50000))
