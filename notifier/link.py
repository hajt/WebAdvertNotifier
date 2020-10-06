from dataclasses import dataclass

@dataclass
class Link:
    """ Url link joiner with the name. """ 

    url: str
    name: str


    def __str__(self) -> str:
        return f'Name: "{self.name}" URL: {self.url}'


    def to_slack_hyperlink(self) -> str:
        """ Function that returns a Slack hyperlink. """
        return f"<{self.url}|{self.name}>"
