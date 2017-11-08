from flask import Flask, render_template, jsonify
<<<<<<< HEAD:app.py
from models import db, Crimes
from sqlalchemy import extract, func, distinct
import os
=======
from sfCrime.models import sfcrime
from sqlalchemy import create_engine
from sfCrime import app

>>>>>>> scroall:sfCrime/app.py

app = Flask(__name__)

@app.route('/')
def index():
    crimes = Crimes.query.with_entities(distinct(Crimes.cat)).all()
    return render_template('map.html', crimes=crimes)

@app.route('/<crime>/<year>')
def geo_json(crime, year):
    points = engine.execute()
    return jsonify({
        'type': 'FeatureCollection',
        'features': [ point.geo_json_point() for point in points ]
    })

@app.route('/agg/month/<crime>/<year>')
def agg_date(crime, year):
    data = Crimes.query.with_entities(
        func.date_trunc('month', Crimes.datetime).label('month'),
        func.count(Crimes.cat)
        ).filter(Crimes.cat == crime
        ).filter(extract('year', Crimes.datetime) == year
        ).group_by('month'
        ).order_by('month'
        ).all()

    return jsonify({
        'crime': crime,
        'aggregates': [ {'date': date, 'occurrences': occurrences}
            for date, occurrences in data ]
    })

@app.route('/agg/day/<crime>/<year>')
def agg_week(crime, year):
    week_days = {
        0: 'Sun',
        1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat'
    }

    data = Crimes.query.with_entities(
        extract('dow', Crimes.datetime).label('day'),
        func.count(Crimes.cat)
        ).filter(Crimes.cat == crime
        ).filter(extract('year', Crimes.datetime) == year
        ).group_by('day'
        ).order_by('day'
        ).all()

    return jsonify({
        'crime': crime,
        'aggregates': [ {'day': week_days[day], 'occurrences': occurences}
            for day, occurences in data ]
    })

