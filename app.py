from flask import Flask, render_template, jsonify
from models import db, Crimes
from sqlalchemy import extract, func
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/<crime>/<year>')
def geo_json(crime, year):
    points = Crimes.query.filter(Crimes.cat == crime
                ).filter(extract('year', Crimes.datetime) == year
                ).all()
    return jsonify({
        'type': 'FeatureCollection',
        'features': [point.geo_json_point() for point in points]
    })

@app.route('/agg/year/<crime>')
def agg_year(crime):
    data = Crimes.query.with_entities(
                extract('year', Crimes.datetime).label('year'),
                func.count(Crimes.cat)).filter(Crimes.cat == crime
                ).group_by('year').order_by('year').all()
    return jsonify({
        'crime': crime,
        'aggregates': [{'year': year, 'occurrences': occurence}
            for year, occurence in data]
    })

@app.route('/agg/day/<crime>')
def agg_week(crime):
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
                func.count(Crimes.cat)).filter(Crimes.cat == crime
                ).group_by('day').order_by('day').all()
    return jsonify({
        'crime': crime,
        'aggregates': [ {'day': week_days[day], 'occurrences': occurence}
            for day, occurence in data ]
    })

if __name__ == '__main__':
    app.run()
