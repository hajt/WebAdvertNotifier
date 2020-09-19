import yaml
import logging

class YamlParser:

    def __init__(self, path):
        try:
            with open(path, 'r') as file:
                try:
                    content = yaml.full_load(file)
                except yaml.YAMLError as err:
                    logging.exception(err)
                else:
                    self.content = content
                    self._validate_content()
                    self._parse_content()
        except FileNotFoundError:
            logging.error(f"No such file or directory: '{path}'")
        except IsADirectoryError:
            logging.error(f"'{path}' is a directory")


    def __str__(self):
        return yaml.dump(self.content, sort_keys=False)


    def __repr__(self):
        return str(self.content)


    def _get_database_config(self):
        key = 'database'
        database = self.content.get(key)    
        if database is None:
            logging.error("No database config data in config file.")
            raise TypeError(f"'{key}' is 'NoneType' object, should be dict()")
        else:
            return database


    def _get_database_path(self):
        key = 'path'
        database = self._get_database_config()
        # print(type(database))
        path = database.get(key)
        if path is None:
            logging.error("No database path in config file.")
            raise ValueError(f"No '{key}' value")
        else:
            return path
                

    def _get_facebook_config(self):
        key = 'facebook'
        facebook = self.content.get(key)    
        if facebook is None:
            logging.error("No facebook config data section in config file.")
            raise TypeError(f"'{key}' is 'NoneType' object, should be dict()")
        else:
            return facebook


    def _get_facebook_email(self):
        key = 'email'
        facebook = self._get_facebook_config()
        email = facebook.get(key)
        if email is None:
            logging.error("No facebook email in config file.")
            raise ValueError(f"No '{key}' value")
        else:
            return email


    def _get_facebook_password(self):
        key = 'password'
        facebook = self._get_facebook_config()
        password = facebook.get(key)
        if password is None:
            logging.error("No facebook password in config file.")
            raise ValueError(f"No '{key}' value")
        else:
            return password


    def _get_facebook_friend_id(self):
        key = 'friend_id'
        facebook = self._get_facebook_config()
        friend_id = facebook.get(key)
        if friend_id is None:
            logging.error("No facebook friend_id in config file.")
            raise ValueError(f"No '{key}' value")
        else:
            return friend_id


    def _get_filters_data(self):
        key = 'filters'
        filters = self.content.get(key)    
        if filters is None:
            logging.error("No filters data section in config file.")
            raise TypeError(f"'{key}' is 'NoneType' object, should be dict()")
        else:
            return filters


    def _get_olx_filters(self):
        key = 'olx'
        filters = self._get_filters_data()
        olx = filters.get(key)
        if olx is None:
            logging.error("No olx filters in config file.")
            raise ValueError(f"No '{key}' values")
        else:
            return olx


    def _validate_content(self):
        if self.content is None:
            logging.error("No config data in config file.")
            raise TypeError(f"'self.content' is 'NoneType' object, should be dict()")
        elif type(self.content) is type(str()):
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'self.content' is str() object, should be dict()")
        elif type(self.content) is type(list()):
            logging.error("Wrong format of config data in config file.")
            raise TypeError(f"'self.content' is list() object, should be dict()")


    def _parse_content(self):
        self.database = self._get_database_config()
        self.database_path = self._get_database_path()
        self.facebook = self._get_facebook_config()
        self.facebook_email = self._get_facebook_email()
        self.facebook_password = self._get_facebook_password()
        self.facebook_friend_id = self._get_facebook_friend_id()
        self.filters = self._get_filters_data()
        self.olx_filters = self._get_olx_filters()


if __name__ == "__main__":
    yaml_file = YamlParser("config.yaml")
    