import argparse
import logging
import sys
import time
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from notifier.models import Base
from notifier.advert_database import AdvertDatabase
from notifier.html_parser import HtmlParser
from notifier.config import ConfigFile
from notifier.slack import Slack
from notifier.logger import log


def construct_database_url(config: ConfigFile) -> str:
    """ Function which returns database url from config data. """
    database_url = f"sqlite:///{config.database_path}"
    return database_url


def setup_database(config: ConfigFile) -> AdvertDatabase:
    """ Function which configure database settings, and returns 
    database_url, engine and session objects. """
    database_url = construct_database_url(config)          
    engine = create_engine(database_url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session() 
    advert_database = AdvertDatabase(database_url, engine, session)
    return advert_database


def setup_slack(config: ConfigFile) -> Slack:
    """ Function which configure Slack to send messages. """
    slack = Slack(config.slack_webhook_url)
    return slack


def create_advert_database(advert_database: AdvertDatabase) -> None:
    """ Function which creates the database if doesn't exist
    and fill her with users and email accounts. """
    if not database_exists(advert_database.database_url):
        log.info('Creating database...')
        create_database(advert_database.database_url)
        Base.metadata.create_all(advert_database.engine)
        log.info('Database created!')


def scan_filters_for_new_adverts(config: ConfigFile, advert_database: AdvertDatabase, slack: Slack) -> None:
    """ Function which scan given website filters for new adverts,
    and updates the database. """
    for portal, links in config.filters.items():
        for link in links:
            html_parser = HtmlParser(link, portal)
            html_parser.parse_and_proccess_page_content(advert_database, slack)


def scan_filters_for_new_adverts_loop(config: ConfigFile, advert_database: AdvertDatabase, slack: Slack, interval: int) -> None:
    """ Function which creates loop with time interval 
    for function scan_filters_for_new_adverts(). """
    while True:
        scan_filters_for_new_adverts(config, advert_database, slack)
        time.sleep(interval)


def create_argparser() -> argparse.Namespace:
    """ Function which creates argparser and return arguments. """
    parser = argparse.ArgumentParser(description='Web Adverts Notifier')
    parser.add_argument("-c", "--collect", action="store_true", help="check stored filters for new adverds")
    parser.add_argument("-i", "--interval", type=int, help="periodically check stored filters for new adverts with provided interval (in seconds)")
    parser.add_argument("--debug", action="store_true", help="debug flag")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args


def notifier_main() -> None:
    """ Main function of notifier. """
    args = create_argparser()
    log.setLevel(logging.DEBUG if args.debug else logging.INFO)

    config = ConfigFile("config.yaml")
    advert_database = setup_database(config)
    slack = setup_slack(config)
    create_advert_database(advert_database)
    
    if args.collect:
        scan_filters_for_new_adverts(config, advert_database, slack)
    elif args.interval:
        scan_filters_for_new_adverts_loop(config, advert_database, slack, args.interval)


if __name__ == "__main__":
    notifier_main()


