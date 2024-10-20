import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from anvil import alert
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


wssh_url = "http://10.215.10.215:8888/"


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


    def filter_and_get_available_values(self, filter_criteria):
        """
        This method filters the list like 'filter_list', but also returns the available values
        for each index (key) in the filter criteria.
        
        :param filter_criteria: A list of dictionaries [{index: [value1, value2, ...]}].
        :return: A dictionary where each key (index) contains the available unique values after filtering.
        """
        # Apply the same filtering logic
        filtered = self.all_lists
        for criterion in filter_criteria:
            for key, values in criterion.items():
                if values:  # If values list is not empty, filter by those values
                    filtered = [item for item in filtered if item[key] in values]

        # Sort the filtered list by the first index (like in filter_list)
        self.filtered_list = sorted(filtered, key=itemgetter(0))

        # Create a dictionary to store the available values for each key (index) in the filter_criteria
        available_values = {}
        for criterion in filter_criteria:
            for key in criterion.keys():
                # Get the unique values for the given index (key) from the filtered_list
                available_values[key] = sorted(set(item[key] for item in self.filtered_list))
        return available_values[3], available_values[4], available_values[10]

    def get_available_values_for_indexes(self, indexes):
        """
        Return the available values for a list of indexes from the filtered_list.
    
        :param indexes: List of indexes to check.
        :return: A dictionary where each index contains the available unique values after filtering.
        """
        available_values = {}
        for index in indexes:
            # Get the unique values for the given index from the filtered_list
            available_values[index] = sorted(set(item[index] for item in self.filtered_list))
    
        return available_values[3], available_values[4], available_values[10]

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
    Filter a list of lists, retaining only the sublists that contain all parts of the specified strings,
    ignoring spaces, and searching only specific indexes.

    Parameters:
    list_of_lists (list of lists): A list containing sublists.
    strings_to_match (str): A string of space-separated words to search for in the sublists.

    Returns:
    list of lists: A filtered list containing only the sublists that have all parts of the strings to match.
    """
    # Define which indexes of sublists can be searched
    indexes_of_interest = [0,2,3,4,5,10]  # You can modify this to fit your use case

    # Split the string to match into words, excluding empty strings or spaces
    words_to_match = [word for word in strings_to_match.lower().split() if word.strip()]
    filtered_list = []

    for sublist in list_of_lists:
        # Ensure all words are matched in the specified items in the sublist
        if all(
            any(word in str(sublist[i]).lower().replace(" ", "") for i in indexes_of_interest if i < len(sublist))
            for word in words_to_match
        ):
            filtered_list.append(sublist)
    
    return filtered_list

def check_if_pmp(data, search_value):
    """
    Check if search_value matches the first item of each list (case insensitive) and
    if the individual list has any truthy value at index 11.
    
    Args:
        data (List[List]): A list of lists to check.
        search_value (str): The value to search for in the first item of each list.

    Returns:
        bool: True if an individual list matches the search value and has a truthy value at index 11.
    """
    for sublist in data:
      # print(sublist[11])
      if (sublist[5].lower() == search_value.lower() or sublist[0].lower() == search_value.lower()) and (sublist[11] != "None" or sublist[5] is not None):
        # print(sublist[11])
        return True
    return False



def wssh_connect(**args):
  url = f"{wssh_url}?hostname={args['sender'].tag.hostname}&username=PMP&password=PMP"
  anvil.js.window.open(url, "_blank")

def manual_connect(**args):
  f = anvil.get_open_form()
  f.manual_hostname_label.text = args['sender'].tag.hostname
  f.ssh_manual_address.text = args['sender'].tag.address
  f.ssh_manual_password.text = ""   
  f.ssh_manual_username.text = ""
  anvil.js.window.scrollTo(0, 0)

def device_table_test_connection(**args):
    
    ping_result = anvil.server.call("ping_host", args["sender"].tag.ip)
    port_result = anvil.server.call("check_port_status", args["sender"].tag.ip, str(22))
    a = f"{ping_result}\n---------------------------------------------------\n\n\n\n SSH PORT STATUS: {port_result}"
    alert(a, title=f"Test Result for {args['sender'].tag.hostname}", large=True)
  
