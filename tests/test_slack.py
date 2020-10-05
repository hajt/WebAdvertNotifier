import unittest
import logging
import json
from unittest.mock import patch
from notifier.slack import Slack


class TestSlack(unittest.TestCase):

    def setUp(self):
        webhook_url = "http://webhook_url.com"
        self.slack = Slack(webhook_url)


    def test_data(self):
        result = self.slack._data('message')
        expected = json.dumps({'text': 'message'})
        self.assertEqual(result, expected)


    @patch('notifier.slack.requests.post')
    def test_send_message_response_code_200(self, mock_requests_post):
        log_message = 'INFO:root:Message succesfully sent!'
        mock_requests_post.return_value.status_code = 200
        with self.assertLogs(level='INFO') as cm:
            self.slack.send_message('message')
        self.assertIn(log_message, cm.output)


    @patch('notifier.slack.requests.post')
    def test_send_message_response_code_not_200(self, mock_requests_post):
        log_message = 'INFO:root:Message cannot be sent.'
        mock_requests_post.return_value.status_code = 404
        with self.assertLogs(level='INFO') as cm:
            self.slack.send_message('message')
        self.assertIn(log_message, cm.output)

    
if __name__ == '__main__':
    unittest.main()
