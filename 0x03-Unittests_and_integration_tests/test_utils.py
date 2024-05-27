#!/usr/bin/env python3
"""utils.access_nested_map_unittest
"""
import unittest
from parameterized import parameterized, param
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """access_nested_map test case"""
    @parameterized.expand([
        param(nested_map={"a": 1}, path=("a",), expected=1),
        param(nested_map={"a": {"b": 2}}, path=("a",), expected={"b": 2}),
        param(nested_map={"a": {"b": 2}}, path=("a", "b"), expected=2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        param(nested_map={}, path=("a",)),
        param(nested_map={"a": 1}, path=("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """test access_nested_map raising the right exception"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
            self.assertEqual(cm.msg, "KeyError: {}".format(path[0]))
