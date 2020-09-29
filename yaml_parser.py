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


    def _get_slack_config(self):
        key = 'slack'
        slack = self.content.get(key)
        self._validate_is_dict(slack)
        return slack 

    
    def _get_slack_webhook_url(self):
        key = 'webhook_url'
        slack = self._get_slack_config()
        webhook_url = slack.get(key)
        self._validate_is_string(webhook_url)
        return webhook_url  


    def _get_logfile_config(self):
        key = 'logfile'
        logfile = self.content.get(key)
        self._validate_is_dict(logfile)
        return logfile    
        

    def _get_logfile_path(self):
        key = 'path'
        logfile = self._get_logfile_config()
        path = logfile.get(key)
        self._validate_is_string(path)
        return path


    def _get_database_config(self):
        key = 'database'
        database = self.content.get(key)
        self._validate_is_dict(database)
        return database    
        

    def _get_database_path(self):
        key = 'path'
        database = self._get_database_config()
        path = database.get(key)
        self._validate_is_string(path)
        return path
                

    def _get_facebook_config(self):
        key = 'facebook'
        facebook = self.content.get(key)    
        self._validate_is_dict(facebook)
        return facebook 


    def _get_facebook_email(self):
        key = 'email'
        facebook = self._get_facebook_config()
        email = facebook.get(key)
        self._validate_is_string(email)
        return email


    def _get_facebook_password(self):
        key = 'password'
        facebook = self._get_facebook_config()
        password = facebook.get(key)
        self._validate_is_string(password)
        return password


    def _get_facebook_friend_id(self):
        key = 'friend_id'
        facebook = self._get_facebook_config()
        friend_id = facebook.get(key)
        self._validate_is_int(friend_id)
        return friend_id


    def _get_filters_data(self):
        key = 'filters'
        filters = self.content.get(key)    
        self._validate_is_dict(filters)
        return filters 


    def _get_olx_filters(self):
        key = 'olx'
        filters = self._get_filters_data()
        olx = filters.get(key)
        self._validate_is_list(olx)
        return olx


    def _parse_content(self):
        self.slack = self._get_slack_config()
        self.slack_webhook_url = self._get_slack_webhook_url()
        self.logfile = self._get_logfile_config()
        self.logfile_path = self._get_logfile_path()
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