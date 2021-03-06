import requests
import re

from bs4 import BeautifulSoup, element
from typing import List, Tuple

from notifier.link import Link
from notifier.advert_database import AdvertDatabase
from notifier.slack import Slack
from notifier.logger import log


class HtmlParser:

    def __init__(self, url: str, portal: str) -> None:
        """ HTML page content parser. """ 
        self.url = url
        self.portal = portal

    
    def _fetch_page_content(self) -> BeautifulSoup:
        """ Function which fetchs HTML page content. """
        log.debug(f"Fetching '{self.url}' content.")
        response = requests.get(self.url)
        log.debug(f"Response code: {str(response.status_code)}")
        if response.status_code == 200:
            content = BeautifulSoup(response.text, "html.parser")
            return content


    def _find_no_adverts_div(self, content: BeautifulSoup) -> element.ResultSet:
        """ Function which search for 'no adverts' div in HTML page content. """
        return content.find_all('div', {'class': 'emptynew emptynew-filters large lheight18'})


    def _find_no_adverts_text(self, content: BeautifulSoup) -> element.ResultSet:
        """ Function which search for all 'no adverts' known 
        text in HTML page content. """
        not_found = re.compile("Nie znaleźliśmy ogłoszeń dla tego zapytania")
        validate_query = re.compile("Sprawdź poprawność albo spróbuj bardziej ogólnego zapytania")
        no_records = re.compile("Brak wyników")
        change_parameters = re.compile("Spróbuj zmienić parametry")
        return content.find_all(string=[not_found, validate_query, no_records, change_parameters])


    def _check_matching_olx_adverts(self, content: BeautifulSoup) -> bool:
        """ Function which checks are matching adverts in HTML page content 
        by checking are 'no adverts div' or 'no adverts text' and returns 
        'True' when not. """
        no_adverts_div = self._find_no_adverts_div(content)
        no_adverts_text = self._find_no_adverts_text(content)
        if no_adverts_div or no_adverts_text:
            return False
        else:
            return True


    def _find_adverts_divs(self, content: BeautifulSoup) -> element.ResultSet:
        """ Function which search for all adverts divs in HTML page content. """
        return content.find_all('div', {'class': "offer-wrapper"})


    def _find_advert_anhor(self, div: element.ResultSet) -> element.Tag:
        """ Function which search for an anhor in div. """
        return div.find('a', {'href': True, 'class': True, 'title': False})

    
    def _get_advert_url_and_name(self, anhor: element.Tag) -> Tuple[str]:
        """ Function which gets url and name from the anhor. """
        url = anhor['href']
        name = anhor.text.strip()
        return url, name
        

    def _get_olx_adverts_links(self, content: BeautifulSoup) -> List[Link]:
        """ Function which extracts anchor links from HTML page content,
        creates Link object with connected url and name of the advert, 
        and returns a list of all found andverts. """
        links = []
        divs = self._find_adverts_divs(content)
        for div in divs:
            anhor = self._find_advert_anhor(div)
            url, name = self._get_advert_url_and_name(anhor)
            advert_link = Link(url, name)
            links.append(advert_link)
        return links


    def _proccess_adverts_links(self, links: List[Link], advert_database: AdvertDatabase, slack: Slack) -> None:
        """ Function which inserts each new advert into the database 
        and send Slack notification. """
        for link in links:
            advert_database.insert_new_advert_and_send_notification(link, slack)


    def proccess_page_content(self, advert_database: AdvertDatabase, slack: Slack) -> None:
        """ Function which fetches HTML page, search in it 
        for the adverts links, store them in the database 
        and send Slack notification. """
        content = self._fetch_page_content()
        if content:
            log.debug(f"Parsing page content...")
            if self.portal == 'olx' and self._check_matching_olx_adverts(content):
                links = self._get_olx_adverts_links(content)
                self._proccess_adverts_links(links, advert_database, slack)
            log.debug(f"Parsing finished.")  
        else:
            log.debug(f"No content to parse.")

