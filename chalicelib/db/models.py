import pymysql
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from chalicelib.conf import settings

pymysql.install_as_MySQLdb()

engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class CurrencyRate(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    base_currency = Column(String(3))
    counter_currency = Column(String(3))
    rate = Column(Float(precision=6))
    created_at = Column(DateTime())

    def __repr__(self):
        return f"<CurrencyRate: {self.base_currency}/{self.counter_currency} - {self.rate}>"

Base.metadata.create_all(engine)
