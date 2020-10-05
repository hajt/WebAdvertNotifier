import unittest
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from notifier.advert_database import AdvertDatabase
from notifier.models import Advert, Base
from notifier.link import Link


class TestAdvertDatabase(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        database_url = 'sqlite:///:memory:'
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session() 
        self.advert_database = AdvertDatabase(database_url, engine, session)
        Base.metadata.create_all(self.advert_database.engine)


    def tearDown(self):
        Base.metadata.drop_all(self.advert_database.engine)
        logging.disable(logging.NOTSET)


    def test_get_advert_no_advert_in_db(self):
        advert = self.advert_database._get_advert_by_url('url')
        self.assertEqual(advert, None)


    def test_get_advert_advert_in_db(self):
        test_advert = Advert(name='name', url='url')
        self.advert_database.session.add(test_advert)
        self.advert_database.session.commit()
        advert = self.advert_database._get_advert_by_url('url')
        self.assertEqual(advert, test_advert)


    def test_save_advert_no_advert_in_db(self):
        link = Link('url', 'name')
        self.advert_database._save_advert(link)
        adverts = self.advert_database.session.query(Advert).all()
        result = len(adverts)
        self.assertEqual(result, 1)


    def test_save_advert_same_advert_already_in_db(self):
        link = Link('url', 'name')
        advert = Advert(name=link.name, url=link.url)
        self.advert_database.session.add(advert)
        self.advert_database.session.commit()
        self.advert_database._save_advert(link)
        adverts = self.advert_database.session.query(Advert).all()
        result = len(adverts)
        self.assertEqual(result, 1)


    def test_insert_new_advert_and_send_notification_no_advert_in_db(self):
        link = Link('url', 'name')
        self.advert_database._save_advert(link)
        adverts = self.advert_database.session.query(Advert).all()
        result = len(adverts)
        self.assertEqual(result, 1)


    def test_insert_new_advert_and_send_notification_advert_in_db(self):
        link1 = Link('url1', 'name1')
        advert1 = Advert(name=link1.name, url=link1.url)
        self.advert_database.session.add(advert1)
        self.advert_database.session.commit()
        link2 = Link('url2', 'name2')
        self.advert_database._save_advert(link2)
        adverts = self.advert_database.session.query(Advert).all()
        result = len(adverts)
        self.assertEqual(result, 2)


    def test_insert_new_advert_and_send_notification_same_advert_already_in_db(self):
        link = Link('url', 'name')
        advert = Advert(name=link.name, url=link.url)
        self.advert_database.session.add(advert)
        self.advert_database.session.commit()
        self.advert_database._save_advert(link)
        adverts = self.advert_database.session.query(Advert).all()
        result = len(adverts)
        self.assertEqual(result, 1)

    
if __name__ == '__main__':
    unittest.main()
