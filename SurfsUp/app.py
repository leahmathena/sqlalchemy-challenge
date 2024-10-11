# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime as dt

#################################################
# Database Setup
#################################################

# Create the engine to connect to the SQLite database
engine = create_engine('sqlite:///C:/Users/leahm/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite')

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Function to get the most recent date
def get_recent_date():
    with Session() as session:
        return session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
        "Welcome to the Climate API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt;<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    recent_date = get_recent_date()
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    with Session() as session:
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precip_dict = {date: prcp for date, prcp in results}
    return jsonify(precip_dict)

@app.route('/api/v1.0/stations')
def stations():
    with Session() as session:
        results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    recent_date = get_recent_date()
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    most_active_station_id = 'USC00519281'  # Most active station ID
    with Session() as session:
        results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= one_year_ago).all()
    tobs_list = [tobs[0] for tobs in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    with Session() as session:
        results = session.query(
            func.min(Measurement.tobs).label("min_temp"),
            func.avg(Measurement.tobs).label("avg_temp"),
            func.max(Measurement.tobs).label("max_temp")
        ).filter(Measurement.date >= start).all()
    temp_stats = [{'min_temp': stat.min_temp, 'avg_temp': stat.avg_temp, 'max_temp': stat.max_temp} for stat in results]
    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    with Session() as session:
        results = session.query(
            func.min(Measurement.tobs).label("min_temp"),
            func.avg(Measurement.tobs).label("avg_temp"),
            func.max(Measurement.tobs).label("max_temp")
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_stats = [{'min_temp': stat.min_temp, 'avg_temp': stat.avg_temp, 'max_temp': stat.max_temp} for stat in results]
    return jsonify(temp_stats)

# Close Session
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()  # This works with scoped_session

if __name__ == '__main__':
    app.run(debug=True)
