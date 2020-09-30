import yaml
import json
from jsonschema import validate, ValidationError
import logging

class YamlParser:

    def __init__(self, path):
        """ Config Yaml file parser class. """ 
        self.content = None
        self.slack_webhook_url = ""
        self.logfile_path = ""
        self.database_path = ""
        self.filters = {}
        self.schema = {
            "type": "object",
            "required": ["slack", "database", "logfile", "filters"],
            "properties": {
                "slack": {
                    "type": "object",
                    "required": ["webhook_url"],
                    "properties": {
                        "webhook_url": {
                            "type": "string"
                        } 
                    }
                },
                "database": {
                    "type": "object",
                    "required": ["path"],
                    "properties": {
                        "path": {
                            "type": "string"
                        } 
                    }
                },
                "logfile": {
                    "type": "object",
                    "required": ["path"],
                    "properties": {
                        "path": {
                            "type": "string"
                        } 
                    }
                },
                "filters": {
                    "type": "object",
                    "required": ["olx"],
                    "properties": {
                        "olx": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        } 
                    }
                }
            }
        }

        try:
            with open(path, 'r') as file:
                try:
                    content = yaml.full_load(file)
                except yaml.YAMLError as err:
                    logging.error(err)
                else:
                    try:
                        validate(content, self.schema)
                    except ValidationError as err:
                        logging.error(err)
                    else:
                        self.content = content
                        self._parse_content()
        except FileNotFoundError:
            logging.error(f"No such file or directory: '{path}'")
        except IsADirectoryError:
            logging.error(f"'{path}' is a directory")


    def __str__(self):
        return yaml.dump(self.content, sort_keys=False)


    def __repr__(self):
        return json.dumps(self.content, sort_keys=False)


    def _get_nested_value(self, *keys):
        """ Function which extract nested value from dict structure. """
        value = self.content
        for key in keys:
            value = value.get(key)
        return value


    def _parse_content(self):
        """ Function which gets and setups needed config data from file content. """
        self.slack_webhook_url = self._get_nested_value('slack', 'webhook_url')
        self.logfile_path = self._get_nested_value('logfile', 'path')
        self.database_path = self._get_nested_value('database', 'path')
        self.filters = self.content.get('filters')
