from flask import Flask, render_template, jsonify
from models import db, Crimes
from sqlalchemy import extract, func, distinct
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)

@app.route('/')
def index():
    crimes = Crimes.query.with_entities(distinct(Crimes.cat)).all()
    return render_template('map.html', crimes=crimes)

@app.route('/<crime>/<year>')
def geo_json(crime, year):
    points = Crimes.query.filter(Crimes.cat == crime
                ).filter(extract('year', Crimes.datetime) == year
                ).all()
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

if __name__ == '__main__':
    app.run()
