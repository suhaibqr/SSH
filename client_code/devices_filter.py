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


class FilterFactory:
    # Shared list between all instances (full dataset)
    _shared_list = []
    _filtered_shared_list = None

    @classmethod
    def set_shared_list(cls, data):
        # Set the initial shared list and make a copy for filtering
        cls._shared_list = sorted(data, key=lambda x: x[0])
        cls._filtered_shared_list = copy.deepcopy(cls._shared_list)

    @classmethod
    def reset_filters(cls):
        # Resets the filtered shared list to the original shared list
        cls._filtered_shared_list = copy.deepcopy(cls._shared_list)

    @classmethod
    def apply_filter(cls, filter_index, filter_value):
        # Apply the filter based on the index and value provided
        if cls._filtered_shared_list is not None:
            cls._filtered_shared_list = [
                item for item in cls._filtered_shared_list
                if item[filter_index] == filter_value
            ]
            cls._filtered_shared_list = sorted(cls._filtered_shared_list, key=lambda x: x[filter_index])

    @classmethod
    def filtered_items(cls, filter_index, filter_value):
        # Get items that match the given filter without affecting shared state
        filtered = [
            item for item in cls._shared_list
            if item[filter_index] == filter_value
        ]
        return sorted(filtered, key=lambda x: x[filter_index])

    @classmethod
    def available_options(cls, index):
        # Get unique values for the given index in the shared list
        if not cls._shared_list:
            return []
        options = list(set(item[index] for item in cls._shared_list if len(item) > index))
        return sorted(options)




