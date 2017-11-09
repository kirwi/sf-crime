from flask import Flask, render_template, jsonify
from sqlalchemy import extract, func, distinct
import os
from sfcrime.models import sfcrime
from sfcrime import app
from sqlalchemy import text

app = Flask(__name__)


@app.route('/')
def index():
    connection = sfcrime.db_init()
    Crimes = connection
    crimes = Crimes.query(sfcrime.sfCrimes.cat).distinct().all()
    return render_template('map.html', crimes=crimes)


@app.route('/<crime>/<year>')
def geo_json(crime, year):
    connection = sfcrime.db_init()
    Crimes = connection
    points = Crimes.query(sfcrime.sfCrimes).filter(sfcrime.sfCrimes.cat == crime).filter(
        extract('year', sfcrime.sfCrimes.datetime) == year).all()

    return jsonify({
        'type': 'FeatureCollection',
        'features': [point.geo_json_point() for point in points]
    })


@app.route('/agg/month/<crime>/<year>')
def agg_date(crime, year):
    """Initializes the database."""
    connection = sfcrime.db_init()
    Crimes = connection

    data = Crimes.query(sfcrime.sfCrimes).with_entities(func.date_trunc('month',
           sfcrime.sfCrimes.datetime).label('month'),
           func.count(sfcrime.sfCrimes.cat)). \
           filter(sfcrime.sfCrimes.cat == crime). \
           filter(extract('year', sfcrime.sfCrimes.datetime) == year). \
           group_by('month').order_by('month').all()

    return jsonify({
        'crime': crime,
        'aggregates': [{'date': date, 'occurrences': occurrences}
                       for date, occurrences in data]
    })


@app.route('/agg/day/<crime>/<year>')
def agg_week(crime, year):
    """lata"""
    connection = sfcrime.db_init()
    Crimes = connection
    week_days = {
        0: 'Sun',
        1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat'
    }
    dow = {
        'Sun': 0,
        'Mon': 1,
        'Tue': 2,
        'Wed': 3,
        'Thu': 4,
        'Fri': 5,
        'Sat': 6
    }
    data = Crimes.query(sfcrime.sfCrimes).with_entities(func.date_trunc('day',
           sfcrime.sfCrimes.datetime).label('day'),
           func.count(sfcrime.sfCrimes.cat)).filter(
           sfcrime.sfCrimes.cat == crime
           ).filter(extract('dow', sfcrime.sfCrimes.datetime) == year
           ).group_by('day').order_by('day').all()

    return jsonify({
        'crime': crime,
        'aggregates': [{'day': dow[day], 'occurrences': occurences}
                       for day, occurences in data]
    })
