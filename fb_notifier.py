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
from yaml_parser import YamlParser


def construct_database_url(config):
    """ Function which returns database url from config data. """
    database_url = f"sqlite:///{config.database_path}"
    return database_url


def setup_database(config):
    """ Function which configure database settings, and returns 
    database_url, engine and session objects. """
    database_url = construct_database_url(config)          
    engine = create_engine(database_url, echo=False)
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
    for portal, links in config.filters.items():
        for link in links:
            html_parser = HtmlParser(link, portal)
            html_parser.parse_page_content(advert_database)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, handlers=[
        logging.FileHandler(filename="fb-notifier.log", mode='w'),
        logging.StreamHandler()
    ])
    logging.getLogger("client").setLevel(logging.INFO)

    config = YamlParser("config.yaml")
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
