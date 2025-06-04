def print_triangle(character, lines):
    for count in range(1, lines + 1):
        print(character * count)

print_triangle(character="@", lines=8)
print_triangle(character="&", lines=13)
print_triangle(character="o", lines=5)

for size in range(1, 21):
    print_triangle(character="#", lines=size)
    print()  #