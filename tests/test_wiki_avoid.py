import unittest
from unittest.mock import patch, MagicMock

import requests
from wikiteam3.dumpgenerator.config import Config
from wikiteam3.utils.wiki_avoid import avoid_robots_disallow


class TestAvoidRobotsDisallow(unittest.TestCase):

    @patch('wikiteam3.utils.wiki_avoid.sys.exit')
    @patch('wikiteam3.utils.wiki_avoid.requests.get')
    @patch('wikiteam3.utils.wiki_avoid.urllib.robotparser.RobotFileParser')
    def test_avoid_robots_disallow_allowed(self, mock_robotparser, mock_requests_get, mock_sys_exit):
        """Test when robots.txt allows the user agent"""
        config = Config()
        config.api = "http://example.com/w/api.php"
        other = MagicMock()
        other.session = requests.Session()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "User-agent: *\nAllow: /"
        mock_requests_get.return_value = mock_response

        mock_bot = MagicMock()
        mock_bot.can_fetch.return_value = True
        mock_robotparser.return_value = mock_bot

        avoid_robots_disallow(config, other)

        mock_requests_get.assert_called_once()
        mock_bot.parse.assert_called_once()
        self.assertEqual(mock_sys_exit.call_count, 0)

    @patch('wikiteam3.utils.wiki_avoid.sys.exit')
    @patch('wikiteam3.utils.wiki_avoid.requests.get')
    @patch('wikiteam3.utils.wiki_avoid.urllib.robotparser.RobotFileParser')
    def test_avoid_robots_disallow_disallowed(self, mock_robotparser, mock_requests_get, mock_sys_exit):
        """Test when robots.txt disallows the user agent"""
        config = Config()
        config.api = "http://example.com/w/api.php"
        other = MagicMock()
        other.session = requests.Session()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "User-agent: wikiteam3\nDisallow: /"
        mock_requests_get.return_value = mock_response

        mock_bot = MagicMock()
        mock_bot.can_fetch.return_value = False
        mock_robotparser.return_value = mock_bot

        avoid_robots_disallow(config, other)

        mock_requests_get.assert_called_once()
        mock_bot.parse.assert_called_once()
        mock_sys_exit.assert_called_once_with(20)

    @patch('wikiteam3.utils.wiki_avoid.sys.exit')
    @patch('wikiteam3.utils.wiki_avoid.requests.get')
    @patch('wikiteam3.utils.wiki_avoid.urllib.robotparser.RobotFileParser')
    def test_avoid_robots_disallow_error(self, mock_robotparser, mock_requests_get, mock_sys_exit):
        """Test when there is an error fetching robots.txt"""
        config = Config()
        config.api = "http://example.com/w/api.php"
        other = MagicMock()
        other.session = requests.Session()

        mock_requests_get.side_effect = Exception("Test exception")

        avoid_robots_disallow(config, other)

        mock_requests_get.assert_called_once()
        self.assertEqual(mock_robotparser.call_count, 1)
        self.assertEqual(mock_sys_exit.call_count, 0)

    @patch('wikiteam3.utils.wiki_avoid.sys.exit')
    @patch('wikiteam3.utils.wiki_avoid.requests.get')
    @patch('wikiteam3.utils.wiki_avoid.urllib.robotparser.RobotFileParser')
    def test_avoid_robots_disallow_robots_not_found(self, mock_robotparser, mock_requests_get, mock_sys_exit):
        """Test when robots.txt returns a 404"""
        config = Config()
        config.api = "http://example.com/w/api.php"
        other = MagicMock()
        other.session = requests.Session()

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        avoid_robots_disallow(config, other)

        mock_requests_get.assert_called_once()
        self.assertEqual(mock_robotparser.call_count, 1)
        self.assertEqual(mock_sys_exit.call_count, 0)

    @patch('wikiteam3.utils.wiki_avoid.sys.exit')
    @patch('wikiteam3.utils.wiki_avoid.requests.get')
    @patch('wikiteam3.utils.wiki_avoid.urllib.robotparser.RobotFileParser')
    def test_avoid_robots_disallow_no_api_index(self, mock_robotparser, mock_requests_get, mock_sys_exit):
        """Test when both config.api and config.index are None"""
        config = Config()
        config.api = None
        config.index = None
        other = MagicMock()
        other.session = requests.Session()

        avoid_robots_disallow(config, other)

        self.assertEqual(mock_requests_get.call_count, 0)
        self.assertEqual(mock_robotparser.call_count, 1)
        self.assertEqual(mock_sys_exit.call_count, 0)

if __name__ == '__main__':
    unittest.main() 