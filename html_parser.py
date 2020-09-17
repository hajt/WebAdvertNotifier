import requests
from bs4 import BeautifulSoup

class Link:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return f"{self.name}: '{self.url}'"


class HtmlParser:

    def __init__(self, url, portal):
        self.url = url
        self.portal = portal

    
    def _fetch_page_content(self):
        request = requests.get(self.url)
        content = BeautifulSoup(request.text, "html.parser")
        return content
    

    def _get_anchor_links(self, content):
        links = []
        divs = content.find_all('div', {'class': "offer-wrapper"})
        for div in divs:
            anhor = div.find('a', {'href': True, 'class': True, 'title': False})
            url = anhor['href']
            name = anhor.text.strip()
            link = Link(name, url)
            links.append(link)
        return links


    def parse_page_content(self, advert_database):
        content = self._fetch_page_content()
        if self.portal == 'olx':
            links = self._get_anchor_links(content)
            for link in links:
                advert_database.insert_new_advert(link)
