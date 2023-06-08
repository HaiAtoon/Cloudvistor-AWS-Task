from typing import List

def count_unique_names(names_list: List[str]) -> int:
    """
    The count_unique_names function takes a list of names and returns the number of unique names in that list.

    :param names_list: Pass in the list of names
    :return: The number of unique names in the list
    """
    unique_names = set()
    for name in names_list:
        names_set = set(x.replace(' ', '') for x in name.lower().split(';'))
        unique_names.update(names_set)
    return len(unique_names)

# Description:
#
# The function starts by creating an empty set of `unique_names` to store the unique names.
# It then loops through each name in the input list, converts it to lowercase using the `lower()` method (In order to be non-case-sensitive), clear any space from the string, and splits it into a list using the `split(';')` method.
# This ensures that each name is clean and separated properly, even if there are multiple names and spaces in a single string.
#
# The function then update the `unique_names` set that was created earlier, with the new set that was just created, by using the `update()` method.
# Since sets only allow unique values, this ensures that only unique names are added to the set.
#
# Finally, the function returns the length of the `unique_names` set, which gives the number of unique non-case-sensitive names in the input list.
#
# This function is efficient because it uses a set to store the unique names, which allows for constant-time lookups and ensures that each name is only added once, even if it appears in multiple strings.
# It also uses built-in Python methods like `lower()` and `split()` to handle string manipulation, which are more efficient than writing custom string parsing code.
#
# In addition, I could implement this function in a more 'Pythonic' way:

def count_unique_names(names_list: List[str]) -> int:
    """
    The count_unique_names function takes a list of names and returns the number of unique names in that list.

    :param names_list: Pass in the list of names
    :return: The number of unique names in the list
    """
    unique_names = set()
    unique_names.update(*[set(x.replace(' ', '') for x in name.lower().split(';')) for name in names_list])
    return len(unique_names)
    
# Here, I use several Pythonic elements, such as Comprehension of a list or set, and unpacking.
# However, this code is less readable, and therefore it's against the 'Zen of Python' rule no. 3 = "Simple is better than complex", and rule no. 7 = "Readability counts".
