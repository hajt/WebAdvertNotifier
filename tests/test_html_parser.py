import unittest
import logging
import json
from unittest.mock import patch
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from notifier.html_parser import HtmlParser
from notifier.link import Link
from notifier.slack import Slack
from notifier.advert_database import AdvertDatabase
from notifier.models import Advert, Base


class TestHtmlParser(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        url = "http://url.com"
        portal = 'olx'
        self.html_paser = HtmlParser(url, portal)


    def tearDown(self):
        logging.disable(logging.NOTSET)

    
    @patch('notifier.html_parser.requests.get')
    def test_fetch_page_content_response_code_not_200(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 404
        content = self.html_paser._fetch_page_content()
        self.assertIsNone(content)


    @patch('notifier.html_parser.requests.get')
    def test_fetch_page_content_response_code_200(self, mock_requests_get):
        requests_text = 'HTML page content'
        test_content = BeautifulSoup(requests_text, "html.parser")
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.text = requests_text
        content = self.html_paser._fetch_page_content()
        self.assertIsNotNone(content)
        self.assertEqual(content, test_content)


    def test_find_no_adverts_div_correct_single_div_in_content(self):
        text = """ 
        <div class="emptynew emptynew-filters large lheight18"></div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_div(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 1)

    
    def test_find_no_adverts_divs_no_div_in_content(self):
        text = ''
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_div(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_div_incorrect_single_div_in_content(self):
        text = """ 
        <div class=""></div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_div(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_div_incorrect_divs_in_content(self):
        text = """
        <div class=""></div>
        <div class="fake emptynew"></div> 
        <div class="emptynew"></div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_div(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_div_correct_and_incorrect_divs_in_content(self):
        text = """
        <div class=""></div>
        <div class="emptynew emptynew-filters large lheight18"></div>
        <div class="fake emptynew"></div> 
        <div class="emptynew"></div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_div(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 1)


    def test_find_no_adverts_text_single_text_in_content(self):
        text = """
        Nie znaleźliśmy ogłoszeń dla tego zapytania.
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_text(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 1)

    
    def test_find_no_adverts_text_no_text_in_content(self):
        text = ''
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_text(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_text_incorrect_single_text_in_content(self):
        text = """ 
        Nie ma ogłoszeń dla tego zapytania.
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_text(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_text_incorrect_text_in_content(self):
        text = """
        Nie ma ogłoszeń dla tego zapytania.
        Nie znaleźliśmy ogłoszeń.
        Sprawdź poprawność albo spróbuj ponownie.
        <div class=""></div>
        <div class="Nie znaleźliśmy ogłoszeń dla tego zapytania."></div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_text(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_no_adverts_text_correct_and_incorrect_text_in_content(self):
        text = """
        Nie znaleźliśmy ogłoszeń dla tego zapytania. 
        Nie ma ogłoszeń dla tego zapytania.
        Nie znaleźliśmy ogłoszeń.
        Sprawdź poprawność albo spróbuj ponownie.
        <div class=""></div>
        <div class="Nie znaleźliśmy ogłoszeń dla tego zapytania."></div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_no_adverts_text(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 1)


    def test_check_matching_olx_adverts_no_adverts_div_and_no_adverts_text_in_content(self):
        text = """
        <div class="emptynew emptynew-filters large lheight18">
        Nie znaleźliśmy ogłoszeń dla tego zapytania.
        </div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._check_matching_olx_adverts(test_content)
        self.assertFalse(status)


    def test_check_matching_olx_adverts_no_adverts_div_and_no_adverts_text_not_in_content(self):
        text = """
        <div>
        Example content.
        </div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._check_matching_olx_adverts(test_content)
        self.assertTrue(status)

    
    def test_check_matching_olx_adverts_no_adverts_div_and_not_no_adverts_text_in_content(self):
        text = """
        <div class="emptynew emptynew-filters large lheight18">
        Example content.
        </div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._check_matching_olx_adverts(test_content)
        self.assertFalse(status)


    def test_check_matching_olx_adverts_not_no_adverts_div_and_no_adverts_text_in_content(self):
        text = """
        <div>
        Nie znaleźliśmy ogłoszeń dla tego zapytania.
        </div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._check_matching_olx_adverts(test_content)
        self.assertFalse(status)
    

    def test_find_adverts_divs_correct_single_div_in_content(self):
        text = """ 
        <div class="offer-wrapper"></div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_adverts_divs(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 1)

    
    def test_find_adverts_divss_no_div_in_content(self):
        text = ''
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_adverts_divs(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_adverts_divs_incorrect_single_div_in_content(self):
        text = """ 
        <div class=""></div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_adverts_divs(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_adverts_divs_incorrect_divs_in_content(self):
        text = """
        <div class=""></div>
        <div class="fake-offer-wrapper"></div> 
        <div class="offer"></div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_adverts_divs(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 0)


    def test_find_adverts_divs_correct_and_incorrect_divs_in_content(self):
        text = """
        <div class="offer-wrapper"></div> 
        <div class=""></div>
        <div class="fake-offer-wrapper"></div> 
        <div class="offer"></div>
        <div class="offer-wrapper"></div> 
        """
        test_content = BeautifulSoup(text, "html.parser")
        status = self.html_paser._find_adverts_divs(test_content)
        result = len(status)
        self.assertIsNotNone(status)
        self.assertEqual(result, 2)

    

    def test_find_advert_anhor_correct_single_anhor_in_div(self):
        text = """ 
        <div>
            <a href="url.com" class="class"></a> 
        <\div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        anhor = self.html_paser._find_advert_anhor(test_content)
        self.assertIsNotNone(anhor)


    def test_find_advert_anhor_incorrect_single_anhor_in_div(self):
        text = """ 
        <div>
            <a href="url.com" class="class" title=""></a> 
        <\div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        anhor = self.html_paser._find_advert_anhor(test_content)
        self.assertIsNone(anhor)


    def test_get_advert_url_and_name(self):
        text = """ 
        <a href="url.com" class="class">Advert</a> 
        """
        test_anhor = BeautifulSoup(text, "html.parser").find('a')
        url, name = self.html_paser._get_advert_url_and_name(test_anhor)
        self.assertEqual(url, 'url.com')
        self.assertEqual(name, 'Advert')


    def test_get_olx_adverts_links_correct_adverts_div(self):
        text = """
        <div class="offer-wrapper">
            <a href="url.com" class="class">Advert</a> 
        <\div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        links = self.html_paser._get_olx_adverts_links(test_content)
        result = len(links)
        self.assertEqual(result, 1) 


    def test_get_olx_adverts_links_incorrect_adverts_div(self):
        text = """
        <div">
            <a href="url.com" class="class" title="">Advert</a> 
        <\div>
        """
        test_content = BeautifulSoup(text, "html.parser")
        links = self.html_paser._get_olx_adverts_links(test_content)
        result = len(links)
        self.assertEqual(result, 0) 


    @patch('notifier.slack.requests.post')
    def test_proccess_adverts_links_valid_links(self, mock_requests_post):
        logging.disable(logging.NOTSET)

        link = Link('url', 'name')
        links = [link]
        
        database_url = 'sqlite:///:memory:'
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session() 
        advert_database = AdvertDatabase(database_url, engine, session)
        Base.metadata.create_all(advert_database.engine)
        
        webhook_url = "http://webhook_url.com"
        slack = Slack(webhook_url)
        
        mock_requests_post.return_value.status_code = 200
        log_message = 'INFO:root:Message succesfully sent!'

        with self.assertLogs(level='INFO') as cm:
            self.html_paser._proccess_adverts_links(links, advert_database, slack)
        self.assertIn(log_message, cm.output)


    @patch('notifier.slack.requests.post')
    @patch('notifier.html_parser.requests.get')
    def test_proccess_page_content_valid_content(self, mock_html_parser_requests_get, mock_slack_requests_post):
        logging.disable(logging.NOTSET)
  
        database_url = 'sqlite:///:memory:'
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session() 
        advert_database = AdvertDatabase(database_url, engine, session)
        Base.metadata.create_all(advert_database.engine)
        
        webhook_url = "http://webhook_url.com"
        slack = Slack(webhook_url)

        requests_text = """
        <div class="offer-wrapper">
            <a href="url.com" class="class">Advert</a> 
        <\div>
        """
        mock_html_parser_requests_get.return_value.status_code = 200
        mock_html_parser_requests_get.return_value.text = requests_text
        mock_slack_requests_post.return_value.status_code = 200
        
        log_message = 'INFO:root:Message succesfully sent!'

        with self.assertLogs(level='DEBUG') as cm:
            self.html_paser.proccess_page_content(advert_database, slack)
        self.assertIn(log_message, cm.output)


    @patch('notifier.html_parser.requests.get')
    def test_proccess_page_content_not_valid_content(self, mock_requests_get):
        logging.disable(logging.NOTSET)
  
        database_url = 'sqlite:///:memory:'
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session() 
        advert_database = AdvertDatabase(database_url, engine, session)
        Base.metadata.create_all(advert_database.engine)
        
        webhook_url = "http://webhook_url.com"
        slack = Slack(webhook_url)

        mock_requests_get.return_value.status_code = 404
        log_message = 'DEBUG:root:No content to parse.'

        with self.assertLogs(level='DEBUG') as cm:
            self.html_paser.proccess_page_content(advert_database, slack)
        self.assertIn(log_message, cm.output)

     
if __name__ == '__main__':
    unittest.main()
