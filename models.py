from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, SmallInteger
from sqlalchemy import UniqueConstraint
import sqlalchemy.orm.exc


Base = declarative_base()

class Advert(Base):
    """ Database 'servers' table model class. """ 
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    url = Column(String(150))

    def __repr__(self):
        return "<Advert(name='%s', url='%s')>" % (self.name, self.url)

