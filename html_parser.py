import requests
import re
from bs4 import BeautifulSoup

class Link:

    def __init__(self, url, name):
        """ Url link joiner with the name. """ 
        self.url = url
        self.name = name


    def __str__(self):
        return f"{self.name}: '{self.url}'"


class HtmlParser:

    def __init__(self, url, portal):
        """ HTML page content parser. """ 
        self.url = url
        self.portal = portal

    
    def _fetch_page_content(self):
        """ Function which fetchs HTML page content. """
        request = requests.get(self.url)
        content = BeautifulSoup(request.text, "html.parser")
        return content


    def _find_no_adverts_div(self, content):
        """ Function which search for 'no adverts' div in HTML page content. """
        return content.find_all('div', {'class': 'emptynew'})


    def _find_no_adverts_text(self, content):
        """ Function which search for all 'no adverts' known 
        text in HTML page content. """
        return content.find_all(string=[re.compile("Nie znaleźliśmy ogłoszeń dla tego zapytania."), re.compile("Sprawdź poprawność albo spróbuj bardziej ogólnego zapytania")])


    def _check_are_matching_adverts(self, content):
        """ Function which checks are matching adverts in HTML page content 
        by checking are 'no adverts div' or 'no adverts text' and returns 
        'True' when not. """
        no_adverts_div = self._find_no_adverts_div(content)
        no_adverts_text = self._find_no_adverts_text(content)
        if no_adverts_div or no_adverts_text:
            return False
        else:
            return True


    def _find_adverts_divs(self, content):
        """ Function which search for all adverts divs in HTML page content. """
        return content.find_all('div', {'class': "offer-wrapper"})


    def _find_advert_anhor(self, div):
        """ Function which search for an anhor in div. """
        return div.find('a', {'href': True, 'class': True, 'title': False})

    
    def _get_advert_url_and_name(self, anhor):
        """ Function which gets url and name from the anhor. """
        url = anhor['href']
        name = anhor.text.strip()
        return url, name
        

    def _get_olx_adverts_links(self, content):
        """ Function which checks are mathing adverts in HTML page content,
        extracts anchor links, creates Link object with connected url and name,
        of the advert, and returns a list of all found andverts. """
        links = []
        if self._check_are_matching_adverts(content):
            divs = self._find_adverts_divs(content)
            for div in divs:
                anhor = self._find_advert_anhor(div)
                url, name = self._get_advert_url_and_name(anhor)
                advert_link = Link(url, name)
                links.append(advert_link)
        return links


    def parse_page_content(self, advert_database, slack):
        """ Function which fetchs HTML page, shearch in them 
        for the adverts links, store them in the database 
        and send Slack notification. """
        content = self._fetch_page_content()
        if self.portal == 'olx':
            links = self._get_olx_adverts_links(content)
            for link in links:
                advert_database.insert_new_advert_and_send_notification(link, slack)
