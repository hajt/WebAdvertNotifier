import yaml
from jsonschema import validate
import logging

class YamlParser:

    def __init__(self, path):

        try:
            with open(path, 'r') as file:
                try:
                    content = yaml.full_load(file)
                except yaml.YAMLError as err:
                    logging.error(err)
                else:
                    self.content = self._validate_is_dict(content)
                    self._parse_content()
        except FileNotFoundError:
            logging.error(f"No such file or directory: '{path}'")
        except IsADirectoryError:
            logging.error(f"'{path}' is a directory")


    def __str__(self):
        return yaml.dump(self.content, sort_keys=False)


    def __repr__(self):
        return str(self.content)


    def _validate_is_dict(self, target):
        if type(target) is type(dict()):
            return target
        else:
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'{type(target).__name__}' object, should be 'dict'")


    def _validate_is_string(self, target):
        if type(target) is type(str()):
            return target
        else:
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'{type(target).__name__}' object, should be 'str'")


    def _validate_is_int(self, target):
        if type(target) is type(int()):
            return target
        else:
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'{type(target).__name__}' object, should be 'int'")


    def _validate_is_list(self, target):
        if type(target) is type(list()):
            return target
        else:
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'{type(target).__name__}' object, should be 'list'")


    def _get_database_config(self):
        key = 'database'
        database = self.content.get(key)
        self._validate_is_dict(database)
        self.database = database    
        

    def _get_database_path(self):
        key = 'path'
        path = self.database.get(key)
        self._validate_is_string(path)
        self.path = path
                

    def _get_facebook_config(self):
        key = 'facebook'
        facebook = self.content.get(key)    
        self._validate_is_dict(facebook)
        self.facebook = facebook 


    def _get_facebook_email(self):
        key = 'email'
        email = self.facebook.get(key)
        self._validate_is_string(email)
        self.email = email


    def _get_facebook_password(self):
        key = 'password'
        password = self.facebook.get(key)
        self._validate_is_string(password)
        self.password = password


    def _get_facebook_friend_id(self):
        key = 'friend_id'
        friend_id = self.facebook.get(key)
        self._validate_is_int(friend_id)
        self.friend_id = friend_id


    def _get_filters_data(self):
        key = 'filters'
        filters = self.content.get(key)    
        self._validate_is_dict(filters)
        self.filters = filters 


    def _get_olx_filters(self):
        key = 'olx'
        olx = self.filters.get(key)
        self._validate_is_list(olx)
        self.olx = olx


    def _parse_content(self):
        self._get_database_config()
        self._get_database_path()
        self._get_facebook_config()
        self._get_facebook_email()
        self._get_facebook_password()
        self._get_facebook_friend_id()
        self._get_filters_data()
        self._get_olx_filters()


if __name__ == "__main__":
    yaml_file = YamlParser("config.yaml")