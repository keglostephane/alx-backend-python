#!/usr/bin/env python3
"""github_org_client_unittest
"""
import unittest
from client import GithubOrgClient
from requests import HTTPError
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, param, parameterized_class
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test GithubOrgClient.public_repos"""
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) \
                as mock__public_repos_url:
            mock_repos_url = TEST_PAYLOAD[0][0]["repos_url"]
            mock__public_repos_url.return_value = mock_repos_url
            mock_get_json.return_value = TEST_PAYLOAD[0][1]
            client = GithubOrgClient("google")
            expected = TEST_PAYLOAD[0][2]

            self.assertEqual(client.public_repos(), expected)
            mock__public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        param(repo={"license": {"key": "my_license"}},
              license_key="my_license", expected=True),
        param(repo={"license": {"key": "other_license"}},
              license_key="my_license", expected=False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ test GithubOrgClient.has_license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {'org_payload': TEST_PAYLOAD[0][0],
     'repos_payload': TEST_PAYLOAD[0][1],
     'expected_repos': TEST_PAYLOAD[0][2],
     'apache2_repos': TEST_PAYLOAD[0][3]},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ integration tests for the GithubOrgClient class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Test case of public repos  method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after tests."""
        cls.get_patcher.stop()
