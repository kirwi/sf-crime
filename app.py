from flask import Flask, render_template, jsonify
from models import db, Crimes
from flask_sqlalchemy import extract

app = Flask(__name__)
db.init_app(app)

@app.route('/')
def index():
    return render_template(map.html)

@app.route('/<crime>/<year>')
def geo_json(crime, year):
    points = Crimes.query \
                .filter(Crimes.cat == crime) \
                .filter(extract('year', Crimes.datetime) == year) \
                .all()
    return jsonify({
        'type': 'FeatureCollection',
        'features': [point.geo_json_point() for point in points]
    })

if __name__ == '__main__':
    app.run()
