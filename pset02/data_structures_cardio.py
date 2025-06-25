import unittest


# get third element from tuple
def third_element(t):
    if not isinstance(t, tuple):
        raise TypeError("input must be a tuple")
    if len(t) < 3:
        raise IndexError("tuple has fewer than 3 elements")
    return t[2]


# reverse a pair of items in tuple
def reverse_pair(t):
    if not isinstance(t, tuple):
        raise TypeError("input must be a tuple")
    if len(t) != 2:
        raise ValueError("tuple must have exactly 2 elements")
    return (t[1], t[0])


# get middle element of list
def middle_element_of_list(a):
    if not isinstance(a, list):
        raise TypeError("input must be a list")
    if len(a) == 0:
        raise IndexError("list is empty")
    mid = (len(a) - 1) // 2
    return a[mid]


# get unique elements from list
def unique_elements(a):
    if not isinstance(a, list):
        raise TypeError("input must be a list")
    return set(a)


# check if list has duplicates
def contains_duplicates(a):
    if not isinstance(a, list):
        raise TypeError("input must be a list")
    return len(set(a)) < len(a)


# check if a is a superset of b
def is_superset(a, b):
    if not isinstance(a, set) or not isinstance(b, set):
        raise TypeError("inputs must be sets")
    return a.issuperset(b)


# check if a is a subset of b
def is_subset(a, b):
    if not isinstance(a, set) or not isinstance(b, set):
        raise TypeError("inputs must be sets")
    return a.issubset(b)


# check if sets have no elements in common
def is_disjoint(a, b):
    if not isinstance(a, set) or not isinstance(b, set):
        raise TypeError("inputs must be sets")
    return a.isdisjoint(b)


# get most frequent value or values in dict
def most_frequent_value_or_values(d):
    if not isinstance(d, dict):
        raise TypeError("input must be a dictionary")
    if not d:
        return None
    counts = {}
    for value in d.values():
        counts[value] = counts.get(value, 0) + 1
    max_count = max(counts.values())
    most_common = {v for v, c in counts.items() if c == max_count}
    if len(most_common) == 1:
        return next(iter(most_common))
    return most_common


# check if key is in both dictionaries
def key_is_in_both_dictionaries(d1, d2, key):
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise TypeError("inputs must be dictionaries")
    return key in d1 and key in d2


# get word frequencies from string
def word_frequencies(s):
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    words = s.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts