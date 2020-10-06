import unittest
import logging
import yaml
from notifier.config import ConfigFile


class ConfigFileTests(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.valid_path = 'tests/testing_config.yaml'
        self.invalid_path = 'invalid_path'
        self.config_file = ConfigFile('tests/testing_config.yaml')


    def tearDown(self):
        logging.disable(logging.NOTSET)


    def test_init_invalid_path(self):
        with self.assertRaises(SystemExit) as cm:
            ConfigFile(self.invalid_path)
        self.assertEqual(cm.exception.code, 0)


    def test_is_file_exist_valid_path(self):
        status = self.config_file._is_file_exist(self.valid_path)
        self.assertEqual(status, True)


    def test_is_file_exist_invalid_path(self):
        status = self.config_file._is_file_exist(self.invalid_path)
        self.assertEqual(status, False)


    def test_validate_valid_yaml_content(self):
        with open(self.valid_path, 'r') as file:
            content = yaml.full_load(file)
        self.config_file._validate_yaml_content(content)


    def test_validate_invalid_yaml_content(self):
        content = {}
        with self.assertRaises(SystemExit) as cm:
            self.config_file._validate_yaml_content(content)
        self.assertEqual(cm.exception.code, 0)


    def test_get_file_content_invalid_path(self):
        with self.assertRaises(SystemExit) as cm:
            self.config_file._get_file_content(self.invalid_path)
        self.assertEqual(cm.exception.code, 0)


    def test_get_file_content_valid_path(self):
        with open(self.valid_path, 'r') as file:
            test_content = yaml.full_load(file)
        content = self.config_file._get_file_content(self.valid_path) 
        self.assertEqual(content, test_content)


    def test_init(self):
        with open(self.valid_path, 'r') as file:
            test_content = yaml.full_load(file)
        test_slack_webhook_url = 'https://test.com'
        test_database_path = 'test.db'
        test_filters = {'olx': ['https://www.olx.pl/test', 'https://www.olx.pl/test2']}
        self.assertEqual(self.config_file.content, test_content)
        self.assertEqual(self.config_file.slack_webhook_url, test_slack_webhook_url)
        self.assertEqual(self.config_file.database_path, test_database_path)
        self.assertEqual(self.config_file.filters, test_filters)
        
        
if __name__ == '__main__':
    unittest.main()

