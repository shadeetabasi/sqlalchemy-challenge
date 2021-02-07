# Now that you have completed your initial analysis, design a Flask API 
# based on the queries that you have just developed.

# Set up Dependencies 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Flask Setup
from flask import Flask, jsonify
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base() 

# reflect the tables
Base.prepare(engine, reflect=True) 

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Routes
#################################################

# /
# Home page
# List all routes that are available
@app.route("/")
def welcome():
    return (
        f"Welcome to Shadee's Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(bind=engine)
    
    last_year_data = engine.execute('select * from measurement where date > "2016-08-23"').fetchall() 
    
    session.close()

    result = {}

    for value in last_year_data:
        date = value[2]
        precipitation = value[3]
    
        if precipitation == None:
            precipitation = 0
        
        if date not in result:
            result[date] = 0
        
        result[date] = result[date] + precipitation

    return jsonify(result)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(bind=engine) 

    active_stations = session.query(station.station).all()

    session.close()

    return jsonify(active_stations)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(bind=engine)

    USC00519281_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date > '2016-08-18').all()
    
    session.close()

    return jsonify(USC00519281_data)

# /api/v1.0/<start>
# Return a JSON list of the minimum temperature, the average temperature, and the max 
# temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and 
# equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(bind=engine)

    start_results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start).\
                        group_by(measurement.date).all()

    session.close()

    return(jsonify(start_results))

# /api/v1.0/<start>/<end>
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between 
# the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_date_end_date(start, end):
    session = Session(bind=engine)

    start_end_results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start, measurement.date <= end).\
                        group_by(measurement.date).all()

    session.close()

    return(jsonify(start_end_results))