# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base= declarative_base()


class Connection():
    def __init__(self):
        self.db_url = "postgresql://localhost:5432/sfcrimes"

    def engine(self):
       return create_engine(self.db_url)
    def session(engine):
       return sessionmaker(bind=engine)


def db_init():
    rt = Connection().engine()
    session=Connection.session(rt)
    return session()


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
