class Person:
    def __init__(self, name, mom=None, dad=None, born=None, died=None):
        self.name = name
        self.mom = mom
        self.dad = dad
        self.born = born
        self.died = died

    def life_span(self):
        return f"{self.born or '?'}-{self.died or '?'}"

    def __str__(self):
        info = f"{self.name} ({self.life_span()})"
        info += f", Mom: {self.mom.name if self.mom else 'Unknown'}"
        info += f", Dad: {self.dad.name if self.dad else 'Unknown'}"
        return info

    def is_sibling_of(self, other):
        same_mom = self.mom is not None and other.mom is not None and self.mom is other.mom
        same_dad = self.dad is not None and other.dad is not None and self.dad is other.dad
        return same_mom or same_dad

    def is_parent_of(self, other):
        return other is not None and (other.mom is self or other.dad is self)

    def is_child_of(self, other):
        return other.is_parent_of(self)

    def is_grandparent_of(self, other):
        return other is not None and (
            (other.mom is not None and self.is_parent_of(other.mom)) or
            (other.dad is not None and self.is_parent_of(other.dad)))

    def get_grandparents(self):
        grandparents = []
        if self.mom:
            if self.mom.mom:
                grandparents.append(self.mom.mom)
            if self.mom.dad:
                grandparents.append(self.mom.dad)
        if self.dad:
            if self.dad.mom:
                grandparents.append(self.dad.mom)
            if self.dad.dad:
                grandparents.append(self.dad.dad)
        return grandparents

    def get_siblings(self):
        siblings = set()
        for parent in (self.mom, self.dad):
            if parent:
                for child in [person for person in globals().values() if isinstance(person, Person)]:
                    if child is not self and parent.is_parent_of(child):
                        siblings.add(child)
        return list(siblings)

    def is_first_cousin_of(self, other):
        my_parents = [self.mom, self.dad]
        other_parents = [other.mom, other.dad]
        for my_parent in my_parents:
            for other_parent in other_parents:
                if my_parent and other_parent and my_parent.is_sibling_of(other_parent):
                    return True
        return False

    def print_family_tree(self, prefix="", level=0):
        indent = "    " * level
        print(f"{prefix}{self.name} ({self.life_span()})")
        if self.mom:
            self.mom.print_family_tree(f"  {indent}mom: ", level + 1)
        if self.dad:
            self.dad.print_family_tree(f"  {indent}dad: ", level + 1)


# people
granbois_7 = Person("Eugénie Granbois", born="bef.1838", died="1907")
baquié_47 = Person("Ferdinand Baquié", born="1837", died="1883")
baquié_46 = Person("Louise Baquié", mom=granbois_7, dad=baquié_47, died="1945")
ramos_1459 = Person("Marie Ramos")
martinez_8709 = Person("Jacques Martinez")
martinez_8708 = Person("Joseph Martinez", mom=ramos_1459, dad=martinez_8709)
martinez_9931 = Person("Adele Martinez", mom=ramos_1459, dad=martinez_8709)
martinez_9927 = Person("Mildred Martinez", mom=baquié_46, dad=martinez_8708)
prevost_1179 = Person("Jeanne Prevost")
fontaine_2773 = Person("Ernest Fontaine")
fontaine_2776 = Person("Suzanne Fontaine", mom=prevost_1179, dad=fontaine_2773)
alioto_37 = Person("Maria Alioto", born="1834", died="aft.1908")
riggitano_1 = Person("Santo Riggitano", born="1824", died="1898")
riggitano_2 = Person("Salvatore Riggitano", mom=alioto_37, dad=riggitano_1)
prevost_1163 = Person("Louis Prevost", mom=fontaine_2776, dad=riggitano_2)
prevost_1162 = Person("Robert Prevost", mom=martinez_9927, dad=prevost_1163)

# test prints
print(prevost_1162)
print(baquié_47.life_span())
print(martinez_9931.life_span())
print(baquié_46.life_span())

# sibling test
print("Are Adele and Joseph siblings?", martinez_9931.is_sibling_of(martinez_8708))

# grandparent test
print("Robert's grandparents:", [p.name for p in prevost_1162.get_grandparents()])

# sibling list test
print("Mildred's siblings:", [p.name for p in martinez_9927.get_siblings()])

# cousin test
print("Is Robert a cousin of Adele?", prevost_1162.is_first_cousin_of(martinez_9931))

# print full tree
print("\nFamily Tree of Robert:")
prevost_1162.print_family_tree()
