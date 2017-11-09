from flask import Flask, render_template, jsonify
from sqlalchemy import extract, func, distinct
import os
from sfCrime.models import sfcrime
from sfCrime import app
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def index():
    connection = sfcrime.db_init()
    Crimes=connection
    crimes = Crimes.query(sfcrime.sfCrimes.cat).distinct().all()
    return render_template('map.html', crimes=crimes)

@app.route('/<crime>/<year>')
def geo_json(crime, year):
    connection = sfcrime.db_init()
    Crimes = connection
    points=Crimes.query(sfcrime.sfCrimes).filter(sfcrime.sfCrimes.cat == crime).filter(extract('year', sfcrime.sfCrimes.datetime) == year).all()

    return jsonify({
        'type': 'FeatureCollection',
        'features': [ point.geo_json_point() for point in points ]
    })

@app.route('/agg/month/<crime>/<year>')
def agg_date(crime, year):
    connection = sfcrime.db_init()
    Crimes = connection
    data=Crimes.query(sfcrime.sfCrimes).with_entities(func.date_trunc('month',
                                    sfcrime.sfCrimes.datetime).label('month'),
                                   func.count(sfcrime.
                                    sfCrimes.cat)).\
                                    filter(sfcrime.sfCrimes.cat == crime). \
                                    filter(extract('year', sfcrime.sfCrimes.datetime) == year).group_by('month').order_by('month').all()

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
    data = Crimes.query(sfcrime.sfCrimes).with_entities(func.date_trunc('dow',
                                          sfcrime.sfCrimes.datetime).label('day'),
                                          func.count(sfcrime.sfCrimes.cat)).filter(sfcrime.sfCrimes.cat == crime
                                                                                   ).filter(extract('year', sfcrime.sfCrimes.datetime) == year
                                                                                            ).group_by('day').order_by('day').all()

    return jsonify({
        'crime': crime,
        'aggregates': [ {'day': week_days[day], 'occurrences': occurences}
            for day, occurences in data ]
    })

