
class AdvertDatabase:

    def __init__(self, database_url, engine, session):
        self.database_url = database_url
        self.engine = engine
        self.session = session

