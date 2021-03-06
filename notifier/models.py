from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()

class Advert(Base):
    """ Database 'adverts' table model class. """ 
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    url = Column(String(150), unique=True)

    def __repr__(self) -> str:
        return f"<Advert(name={self.name}, url={self.url})>"

