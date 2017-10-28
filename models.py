from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Crimes(db.Model):
    __tablename__ = 'sfcrimes'

    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.Text, index=True)
    descr = db.Column(db.Text)
    dist = db.Column(db.Text)
    datetimte = db.Column(db.DateTime, index=True)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)

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
