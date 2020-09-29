import sqlalchemy.exc
import sqlalchemy.orm.exc
import logging
from models import Advert


class AdvertDatabase:

    def __init__(self, database_url, engine, session):
        """ Database 'adverts' table model class. """ 
        self.database_url = database_url
        self.engine = engine
        self.session = session


    def _get_advert_by_url(self, url):
        """ Function that's query the database for advert by url, and returns 
        Advert object if exist or raises Exception, when error occurs. """
        return self.session.query(Advert).filter(Advert.url==url).scalar()


    def _store_advert(self, link):
        """ Function that's creates Advert object, and save to the database. """
        advert = Advert(name=link.name, url=link.url)
        self.session.add(advert)
        try:
            self.session.commit()
            logging.info(f"Inserted advert into database '{link.url}'")
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            logging.error(f"There is already same advert in 'adverts' table.\nInvolved url: '{link.url}'")


    def insert_new_advert_and_send_notification(self, link, slack):
        """ Function which inserts new advert into database and sends  
        Slack notification message. """
        try:
            advert = self._get_advert_by_url(link.url)
        except sqlalchemy.orm.exc.MultipleResultsFound:
            logging.error(f"Multiple adverts '{link.url}' found in 'adverts' table.")
        else:      
            if not advert:
                logging.info(f"Found new advert: {link.name} - '{link.url}'" )
                self._store_advert(link)
                slack.send_message(link)



