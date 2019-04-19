from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Float, DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class Winery(Base):
    __tablename__ = 'wineries'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, on_updated=func.now())

    styles = relationship('WineStyle', secondary=winery_style)


class WineStyle(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, on_updated=func.now())

    wineries = relationship('Winery', secondary=winery_style)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False) # TODO make sure password is hashed
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, on_updated=func.now())


winery_style = Table('winery_styles', Base.metadata,
                     Column('winery_id'), Integer, ForeignKey('wineries.id'),
                     Column('style_id'), Integer, ForeignKey('styles.id'))
