def move(n, source, destination, auxiliary):
    if n > 0:
        move(n - 1, source, auxiliary, destination)
        print(f"Move disk {n} from {source} to {destination}")
        move(n - 1, auxiliary, destination, source)


def main():
    try:
        number_of_disks = int(input("Enter the number of disks (1 to 20): "))

        if number_of_disks < 1 or number_of_disks > 20:
            raise ValueError("The number must be between 1 and 20, inclusive.")

        move(number_of_disks, "A", "B", "C")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
