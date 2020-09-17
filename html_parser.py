import requests
from bs4 import BeautifulSoup


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
            anhor = div.find('a', {'href': True, 'class': True})
            links.append(anhor['href'])
        return links
        # anchors = []
        # links = content.find_all('a', {'class': 'thumb vtop inlblk rel tdnone linkWithHash scale4 detailsLink', 'href': True})
        # for link in links:
        #     anchors.append(link['href'])
        # return anchors

    def parse_page_content(self):
        content = self._fetch_page_content()
        if self.portal == 'olx':
            links = self._get_anchor_links(content)
            print(links)
        

if __name__ == "__main__":

    html = HtmlParser("https://www.olx.pl/motoryzacja/samochody/bmw/q-m-pakiet/?search%5Bfilter_float_price%3Ato%5D=5000&search%5Bfilter_enum_model%5D%5B0%5D=3-as-sorozat&search%5Bfilter_enum_car_body%5D%5B0%5D=estate-car", "olx")
    html.parse_page_content()
