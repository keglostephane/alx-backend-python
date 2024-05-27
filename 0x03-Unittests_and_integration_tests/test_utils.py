#!/usr/bin/env python3
"""utils.access_nested_map_unittest
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized, param
from utils import access_nested_map, get_json, memoize


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


class TestGetJson(unittest.TestCase):
    """get_json test case"""
    @parameterized.expand([
        param(test_url="http://example.com", test_payload={"payload": True}),
        param(test_url="http://holberton.io", test_payload={"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, mock_get, test_url, test_payload):
        """test get_json"""
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """memoize test case"""
    def test_memoize(self):
        """test memoize"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = "mocked"
            test = TestClass()
            value1 = test.a_property
            value2 = test.a_property
            self.assertEqual(value1, "mocked")
            self.assertEqual(value2, "mocked")
            mock_a_method.assert_called_once()
