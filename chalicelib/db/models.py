import pymysql
from sqlalchemy import (Boolean, Column, DateTime, Float, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from chalicelib.conf import settings

pymysql.install_as_MySQLdb()

engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    base = Column(String(3), index=True)
    counter = Column(String(3), index=True)
    last = Column(Float(precision=6))
    created_at = Column(DateTime(), index=True)

    def __repr__(self):
        return f"<Currency: {self.base}/{self.counter} - {self.rate}>"


class Ticker(Base):
    __tablename__ = 'tickers'

    id = Column(Integer, primary_key=True)
    exchange = Column(String(64), index=True)
    base = Column(String(5), index=True)
    counter = Column(String(5), index=True)
    last = Column(Float(precision=8))
    lowest_ask = Column(Float(precision=8))
    highest_bid = Column(Float(precision=8))
    percent_change = Column(Float(precision=8))
    base_volume = Column(Float(precision=8))
    quote_volume = Column(Float(precision=8))
    is_frozen = Column(Boolean)
    highest_24h = Column(Float(precision=8))
    lowest_24h = Column(Float(precision=8))
    created_at = Column(DateTime(), index=True)

    def __repr__(self):
        return f"<CurrencyRate: {self.base}/{self.counter} - {self.last}>"

Base.metadata.create_all(engine)
