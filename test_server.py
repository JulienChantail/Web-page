#!/usr/bin/env python3

"""
This module contains unit tests for the `safeget` function.
The `safeget` function allows safe retrieval of values from nested dictionaries or lists.
"""

import unittest

def safeget(dct, *keys):
    """
    Safely retrieve a value from a nested dictionary or list.

    :param dct: The dictionary or list to retrieve the value from.
    :param keys: A sequence of keys or indices to traverse.
    :return: The retrieved value or None if the path does not exist.
    """
    for key in keys:
        if isinstance(dct, dict) and key in dct:
            dct = dct[key]
        elif isinstance(dct, list) and isinstance(key, int) and 0 <= key < len(dct):
            dct = dct[key]
        else:
            return None
    return dct

class TestSafeget(unittest.TestCase):
    """
    Unit tests for the `safeget` function.
    """

    def test_safeget_existing_key(self):
        """
        Test retrieving an existing key from a nested dictionary.
        """
        dct = {'user': {'name': 'John', 'email': 'john@example.com'}}
        result = safeget(dct, 'user', 'email')
        self.assertEqual(result, 'john@example.com')

    def test_safeget_non_existing_key(self):
        """
        Test retrieving a non-existing key from a nested dictionary.
        """
        dct = {'user': {'name': 'John'}}
        result = safeget(dct, 'user', 'email')
        self.assertIsNone(result)

    def test_safeget_nested_key(self):
        """
        Test retrieving a deeply nested key.
        """
        dct = {'settings': {'preferences': {'theme': 'dark', 'notifications': True}}}
        result = safeget(dct, 'settings', 'preferences', 'theme')
        self.assertEqual(result, 'dark')

    def test_safeget_deeply_nested_missing_key(self):
        """
        Test retrieving a missing key in a deeply nested dictionary.
        """
        dct = {'settings': {'preferences': {'theme': 'dark'}}}
        result = safeget(dct, 'settings', 'preferences', 'notifications')
        self.assertIsNone(result)

    def test_safeget_empty_dictionary(self):
        """
        Test retrieving from an empty dictionary.
        """
        dct = {}
        result = safeget(dct, 'some', 'nonexistent', 'path')
        self.assertIsNone(result)

    def test_safeget_top_level_key(self):
        """
        Test retrieving a top-level key.
        """
        dct = {'top': 42}
        result = safeget(dct, 'top')
        self.assertEqual(result, 42)

    def test_safeget_type_handling(self):
        """
        Test retrieving a value with non-dictionary types.
        """
        dct = {'key': [1, 2, 3]}
        result = safeget(dct, 'key')
        self.assertEqual(result, [1, 2, 3])

    def test_safeget_invalid_path(self):
        """
        Test retrieving with an invalid path.
        """
        dct = {'valid': {'path': {'key': 'value'}}}
        result = safeget(dct, 'valid', 'invalid', 'key')
        self.assertIsNone(result)

    def test_safeget_with_non_dict_intermediate(self):
        """
        Test retrieving with an intermediate value that is not a dictionary or list.
        """
        dct = {'key': 'not_a_dict'}
        result = safeget(dct, 'key', 'subkey')
        self.assertIsNone(result)

    def test_safeget_mixed_type_path(self):
        """
        Test retrieving a value using a mixed type path (list and dictionary).
        """
        dct = {'list': [{'key': 'value'}]}
        result = safeget(dct, 'list', 0, 'key')
        self.assertEqual(result, 'value')

if __name__ == '__main__':
    unittest.main()
