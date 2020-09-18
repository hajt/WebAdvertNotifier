import yaml
import logging
import fbchat
from fbchat.models import Message, ThreadType
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from advert_database import AdvertDatabase
from html_parser import HtmlParser


def construct_database_url(config):
    """ Function which returns database url from config data. """
    database = config.get('database')    
    if database is None:
        logging.error("No database config data section in config file.")
        raise KeyError("No such key 'database' in config file")
    else:
        path = database.get('path')
        database_url = f"sqlite:///{path}"
        return database_url


def setup_database(config):
    """ Function which configure database settings, and returns 
    database_url, engine and session objects. """
    database_url = construct_database_url(config)
    if database_url is None:
        logging.error("Wrong 'database_url' type.")
        raise TypeError("'database_url' is 'NoneType', but should be 'str'")
    else:                
        engine = create_engine(database_url, echo=True)
            
        Session = sessionmaker(bind=engine)
        session = Session() 
        advert_database = AdvertDatabase(database_url, engine, session)
        return advert_database


def create_advert_database(advert_database):
    """ Function which creates the database if doesn't exist
    and fill her with users and email accounts. """
    if not database_exists(advert_database.database_url):
        logging.info('Creating database...')
        create_database(advert_database.database_url)
        Base.metadata.create_all(advert_database.engine)
        logging.info('Database created!')


def scan_filters_for_new_adverts(config, advert_database):
    """ Function which scan given website filters for new adverts,
    and updates the database. """
    filters = config.get('filters')
    if filters is None:
        logging.error("No filters found in config file.")
        raise KeyError("No such key 'filters' in config file")
    else:
        for portal, links in filters.items():
            for link in links:
                html_parser = HtmlParser(link, portal)
                html_parser.parse_page_content(advert_database)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, handlers=[
        logging.FileHandler(filename="fb-notifier.log", mode='w'),
        logging.StreamHandler()
    ])
    logging.getLogger("client").setLevel(logging.INFO)

    with open("config.yaml", 'r') as config_file:
        try:
            config = yaml.full_load(config_file)
        except yaml.YAMLError as err:
            logging.exception(err)
        else:
            advert_database = setup_database(config)
            create_advert_database(advert_database)
            scan_filters_for_new_adverts(config, advert_database)


            # fb_conf = config.get('facebook')
            # email = fb_conf.get('email')
            # password = fb_conf.get('password')
            # friend_id = fb_conf.get('friend_id')
            # text = "Test MESSAGE"
            # client = fbchat.Client(email, password) 
            # client.send(Message(text=text), thread_id=friend_id, thread_type=ThreadType.USER)
            # client.logout()
