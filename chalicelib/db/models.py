import pymysql
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Numeric,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from chalicelib.conf import settings
from chalicelib.db.mixins import BaseMixin

pymysql.install_as_MySQLdb()

engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(cls=BaseMixin)


class Currency(Base):
    __tablename__ = 'currencies'

    base = Column(String(3), index=True)
    counter = Column(String(3), index=True)
    last = Column(Numeric(precision=12, scale=6))

    def __repr__(self):
        return f"<Currency: {self.base}/{self.counter} - {self.last}>"


class Ticker(Base):
    __tablename__ = 'tickers'

    exchange = Column(String(64), index=True)
    base = Column(String(5), index=True)
    counter = Column(String(5), index=True)
    last = Column(Numeric(precision=15, scale=8))
    lowest_ask = Column(Numeric(precision=15, scale=8))
    highest_bid = Column(Numeric(precision=15, scale=8))
    percent_change = Column(Numeric(precision=10, scale=8))
    base_volume = Column(Numeric(precision=18, scale=8))
    quote_volume = Column(Numeric(precision=18, scale=8))
    is_frozen = Column(Boolean)
    highest_24h = Column(Numeric(precision=15, scale=8))
    lowest_24h = Column(Numeric(precision=15, scale=8))

    def __repr__(self):
        return f"<Ticker: {self.base}/{self.counter} - {self.last}>"


class Chat(Base):
    __tablename__ = 'chats'

    telegram_chat_id = Column(Integer, unique=True, index=True)
    chat_type = Column(String(64))
    title = Column(String(128))
    username = Column(String(128))
    first_name = Column(String(128))
    last_name = Column(String(128))
    all_members_are_administrators = Column(Boolean)
    description = Column(String(128))
    invite_link = Column(String(128))

    def __repr__(self):
        return f"<Chat: {self.chat_id}/{self.first_name}{self.last_name}/{self.username}>"


class Alert(Base):
    __tablename__ = 'alerts'

    chat_id = Column(Integer, ForeignKey('chats.id'), index=True)
    base = Column(String(5))
    counter = Column(String(5))
    expression = Column(String(5))
    value = Column(Numeric(precision=18, scale=8))
    is_active = Column(Boolean, default=True, index=True)

    chat = relationship("Chat", back_populates="alerts")

    def __repr__(self):
        return f"Alert {self.id}: {self.base}/{self.counter} {self.expression} {self.value}"

Chat.alerts = relationship("Alert", order_by=Alert.id, back_populates="chat")

Base.metadata.create_all(engine)
