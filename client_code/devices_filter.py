import anvil.server
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

import json
import copy
from operator import itemgetter

class FilterFactory:
    def __init__(self, all_lists):
        # Download the data from the given URL and store it in all_lists
        self.all_lists = all_lists
        self.filtered_list = sorted(self.all_lists, key=itemgetter(0))

    def filter_list(self, filter_criteria):
        """
        Filter the list based on a given list of dictionary criteria [{index: [value1, value2, ...]}].
        """
        filtered = self.all_lists
        for criterion in filter_criteria:
            for key, values in criterion.items():
                if values:  # If values list is not empty, filter by those values
                    filtered = [item for item in filtered if item[key] in values]
        self.filtered_list = sorted(filtered, key=itemgetter(0))

    def get_available_values(self, index):
        """
        Return the available values for the given index from the filtered_list.
        """
        return sorted(set(item[index] for item in self.filtered_list))



def list_of_lists_to_dicts(keys, list_of_lists, indexes_of_interest):
    """
    Convert a list of lists to a list of dictionaries.

    Parameters:
    keys (list): A list of keys for the dictionaries.
    list_of_lists (list of lists): A list containing sublists, which have values for the dictionaries.
    indexes_of_interest (list): A list of indexes from the sublists to be used as values.

    Returns:
    list of dicts: A list containing dictionaries constructed from the given keys and values.

    # Example usage
    keys = ["name", "age"]
    list_of_lists = [["Alice", 25, "Engineer"], ["Bob", 30, "Designer"], ["Charlie", 22, "Doctor"]]
    indexes_of_interest = [0, 1]
    
    result = list_of_lists_to_dicts(keys, list_of_lists, indexes_of_interest)
    print(result)
    # Output: [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Charlie', 'age': 22}]

    
    """
    list_of_dicts = []
    for sublist in list_of_lists:
        selected_values = [sublist[i] for i in indexes_of_interest]
        dictionary = dict(zip(keys, selected_values))
        list_of_dicts.append(dictionary)
    return list_of_dicts

def filter_list_of_lists_by_strings(list_of_lists, strings_to_match):
    """
    Filter a list of lists, retaining only the sublists that contain any part of the specified strings.

    Parameters:
    list_of_lists (list of lists): A list containing sublists.
    strings_to_match (str): A string of space-separated words to search for in the sublists.

    Returns:
    list of lists: A filtered list containing only the sublists that have any part of the strings to match.
    """
    words_to_match = strings_to_match.lower().split()
    filtered_list = []
    for sublist in list_of_lists:
        if any(any(word in str(item).lower() for word in words_to_match) for item in sublist):
            filtered_list.append(sublist)
    return filtered_list