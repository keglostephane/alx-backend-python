#!/usr/bin/env python3
"""github_org_client_unittest
"""
import unittest
from client import GithubOrgClient
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, param
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """GitHubOrgClient test case"""
    @parameterized.expand([
        param(org="google", result={"login": "google", "id": 1}),
        param(org="abc", result={})
    ])
    @patch('client.get_json')
    def test_org(self, get_json_mock, org, result):
        """test GitHubOrgClient org method"""
        get_json_mock.return_value = result
        url = f"https://api.github.com/orgs/{org}"
        client = GithubOrgClient(org)
        self.assertEqual(client.org, result)
        get_json_mock.assert_called_once_with(url)

    def test_public_repos_url(self):
        """test GithubOrgClient._public_repos_url"""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = TEST_PAYLOAD[0][0]
            client = GithubOrgClient("google")
            expected = "https://api.github.com/orgs/google/repos"
            self.assertEqual(client._public_repos_url, expected)
