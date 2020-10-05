from dataclasses import dataclass

@dataclass
class Link:
    """ Url link joiner with the name. """ 

    url: str
    name: str


    def __str__(self) -> str:
        return f"Name: '{self.name}', Url: '{self.url}'"