import yaml
import json
import jsonschema
import os
import sys

from typing import Union, Dict, List, Optional

from notifier.logger import log


class ConfigFile:
    _schema_path = 'schema.json'

    def __init__(self, path: str) -> None:
        """ Config YAML file class. """ 
        self.schema = self._get_schema()
        self.content = self._get_file_content(path)
        self.slack_webhook_url = self.content['slack']['webhook_url']
        self.database_path = self.content['database']['path']
        self.filters = self.content['filters']


    def __str__(self) -> str:
        return yaml.dump(self.content, sort_keys=False)


    def __repr__(self) -> str:
        return json.dumps(self.content, sort_keys=False)


    def _is_file_exist(self, path: str) -> bool:
        """ Function which checks is file exists. """
        log.debug(f"Checking is '{path}' file exists.")
        return os.path.isfile(path)

    
    def _get_schema(self) -> Optional[Dict[str, Dict[str, Union[str, List[str]]]]]:
        """ Function which reads json schema file and returns content, 
        or raises excepion when schema file doesn't exists. """
        if self._is_file_exist(self._schema_path):
            with open(self._schema_path, 'r') as file:
                content = json.load(file)
                return content
        else:
            raise FileNotFoundError("No schema file found.")


    def _validate_yaml_content(self, content: Dict[str, Dict[str, Union[str, List[str]]]]) -> Optional[SystemExit]:
        """ Function which validates config file content with schema,
        and exits program when exception occours. """
        log.debug("Validating config file...")
        try:
            jsonschema.validate(content, self.schema)
        except jsonschema.ValidationError as err:
            log.error(err)
            sys.exit(0)
        log.debug("Validation succeeded!")


    def _get_file_content(self, path: str) -> Union[Dict[str, Dict[str, Union[str, List[str]]]], SystemExit]:
        """ Function which reads config file, checks is validate and 
        returns content, or exit program when config file doesn't exists. """
        if self._is_file_exist(path):
            with open(path, 'r') as file:
                content = yaml.full_load(file)
                self._validate_yaml_content(content)
                return content
        else:
            log.error(f"Not found '{path}' file.")
            sys.exit(0)
