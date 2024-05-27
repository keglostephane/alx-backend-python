#!/usr/bin/env python3
"""github_org_client_unittest
"""
import unittest
from client import GithubOrgClient
from unittest.mock import patch, Mock
from parameterized import parameterized, param
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """GitHubOrgClient test case"""
    @parameterized.expand([
        param(org="google", result={"login": "google", "id": 1}),
        param(org="abc", result={})
    ])
    @patch('client.get_json')
    def test_org(self, get_json_mock: Mock, org: str, result: Dict):
        """test GitHubOrgClient org method"""
        get_json_mock.return_value = result
        url = f"https://api.github.com/orgs/{org}"
        client = GithubOrgClient(org)
        self.assertEqual(client.org, result)
        get_json_mock.assert_called_once_with(url)
