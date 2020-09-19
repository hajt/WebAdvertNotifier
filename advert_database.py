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
        Advert object if exist or None when don't or exception occurs. """
        try:
            return self.session.query(Advert).filter(Advert.url==url).scalar()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            logging.error(f"Multiple adverts '{url}' found in 'adverts' table.")


    def insert_new_advert(self, link):
        """ Function which inserts new advert into database, when it doesn't exist. """
        advert = self._get_advert_by_url(link.url)
        if not advert:
            logging.info(f"Found new advert: {link.name} - '{link.url}'" )
            advert = Advert(name=link.name, url=link.url)
            self.session.add(advert)
            try:
                self.session.commit()
                logging.info(f"Inserted advert into database '{link.url}'")
            except sqlalchemy.exc.IntegrityError:
                self.session.rollback()
                logging.error(f"There is already same advert in 'adverts' table.\nInvolved url: '{link.url}'")
