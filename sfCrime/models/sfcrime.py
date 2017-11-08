# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base= declarative_base()


class Connection():
    def __init__(self):
        self.db_url = url="postgresql+psycopg2://localhost:5432/sfcrimes"
    def url(self):
        return self.db_url
    def engine(url=url()):
       return create_engine(url)
    def session(engine):
       return sessionmaker(bind=engine)
    def connection(session):
       return session()
    def link(self):




class sfCrimes(Base):
    __tablename__ = 'sfcrimes'

    id = Column(Integer, primary_key=True)
    cat = Column(Text, index=True)
    descr = Column(Text)
    dist = Column(Text)
    datetime = Column(DateTime, index=True)
    lng = Column(Float)
    lat = Column(Float)

    def __repr__(self):
        return "<Crime(id='%s', datetime='%s', cat='%s')>" % (
            self.id, self.datetime, self.cat)

    def geo_json_point(self):
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.lng, self.lat]
            },
            'properties': {
                'crime': self.cat,
                'descr': self.descr,
                'dist': self.dist,
                'datetime': self.datetime
            }
        }
