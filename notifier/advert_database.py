import sqlalchemy.exc
import sqlalchemy.orm.exc

from notifier.logger import log
from notifier.models import Advert
from notifier.link import Link
from notifier.slack import Slack


class AdvertDatabase:

    def __init__(self, database_url: str, engine: sqlalchemy.engine.base.Engine, session: sqlalchemy.orm.session.Session) -> None:
        """ Database 'adverts' table model class. """ 
        self.database_url = database_url
        self.engine = engine
        self.session = session


    def _get_advert_by_url(self, url: str) -> Advert: 
        """ Function that's query the database for advert by url, and returns 
        Advert object if exist or raises Exception, when error occurs. """
        return self.session.query(Advert).filter(Advert.url==url).scalar()


    def _save_advert(self, link: Link) -> None:
        """ Function that's creates Advert object, and save to the database. """
        advert = Advert(name=link.name, url=link.url)
        self.session.add(advert)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            log.warning(f"There is already same advert in 'adverts' table.\nInvolved url: '{link.url}'")
        else:
            log.debug(f"Saved advert in database.")


    def insert_new_advert_and_send_notification(self, link: Link, slack: Slack) -> None:
        """ Function which inserts new advert into database and sends  
        Slack notification message. """
        try:
            advert = self._get_advert_by_url(link.url)
        except sqlalchemy.orm.exc.MultipleResultsFound:
            log.error(f"Multiple adverts '{link.url}' found in 'adverts' table.")
        else:      
            if not advert:
                log.info(f"Found new advert: '{link.name}' - '{link.url}'" )
                self._save_advert(link)
                hyperlink = link.to_slack_hyperlink()
                slack.send_message(hyperlink)
