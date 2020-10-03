import requests
import json
from logger import log

class Slack():

    def __init__(self, webhook_url):
        """ Slack sender notifications class. """ 
        self.webhook_url = webhook_url
        self.headers = {'Content-Type': 'application/json'}


    def _data(self, text):
        """ Message text wrapper for request.post(data) argument. """
        return json.dumps({'text': f'{text}'})


    def send_message(self, text):
        """ Function which sends Slack message as HTTP POST request. """ 
        log.info("Sending message...")
        response = requests.post(self.webhook_url, data=self._data(text), headers=self.headers)
        log.debug(f"Response code: {str(response.status_code)}")
        if response.status_code==200:
            log.info("Message succesfully sent!")
        else:
            log.info("Message cannot be sent.")


