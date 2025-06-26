# pyramid blocks calculation using formula
def blocks(n):
    return n * (n + 1) // 2 if n > 0 else 0


# sum of digits using a loop
def sum_of_digits(n):
    n = abs(n)  # handle negative numbers
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


# factorial using a loop
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# is_palindrome using a loop
def is_palindrome(s):
    return s == s[::-1]


# print countdown using a loop
def print_count_down(n):
    for i in range(n, 0, -1):
        print(i)
    print("BOOM")


# test cases
if __name__ == "__main__":
    print("blocks tests")
    print(blocks(8))      # 36
    print(blocks(0))      # 0
    print(blocks(-1))     # 0
    print(blocks(1))      # 1
    print(blocks(838852)) # works perfectly

    print("\nsum_of_digits tests")
    print(sum_of_digits(1234))     # 10
    print(sum_of_digits(-48729))   # 30
    print(sum_of_digits(0))        # 0

    print("\nfactorial tests")
    print(factorial(5))   # 120
    print(factorial(0))   # 1
    print(factorial(1))   # 1

    print("\nis_palindrome tests")
    print(is_palindrome("racecar"))  # True
    print(is_palindrome("hello"))    # False
    print(is_palindrome("a"))        # True
    print(is_palindrome(""))         # True

    print("\nprint_count_down test")
    print_count_down(5)  # prints 5 to BOOM
