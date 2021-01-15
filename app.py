# Import Dependencies
# YOUR CODE HERE
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import dateutil.parser

##Database Setup##
engine = create_engine("sqlite:///hawaii.sqlite")
#Reflect an existing database into a new model
Base =  automap_base()
#Reflect the tables
Base.prepare(engine, reflect = True)

#Save references to the table 
Measurement = Base.classes.measurement
Station = Base.classes.station

##Flask Routes##
from flask import Flask, jsonify
app = Flask(__name__)

#Route to Home page
@app.route("/")
# List all routes that are available.
def home ():
    return(
        f"Aloha! Welcome to HI's Climate API!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )
# Create route: /api/v1.0/precipitation
@app.route('/api/v1.0/precipitation')
#Create session link from Python to the database
def precipitation():
    session = Session(engine)
    #Query results of precipitation and date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime(Measurement.date >= query_date)).all()
    session.close()
    #Create a dictionary from the row data and append to a list of records
    precip_records = []
    for Measurement.date, Measurement.prcp in results:
        precip_dict={}
        precip_dict["date"] = Measurement.date
        precip_dict["precipitation"] = Measurement.prcp
        precip_records.append(precip_dict)
    #Return the JSON representation of the dictionary
    return jsonify(precip_records)

        
# Create route /api/v1.0/stations
@app.route('/api/v1.0/stations')
#Create session link from Python to the database
def stations():
    session = Session(engine)
    #Query results of stations and their observation counts
    station_ordered_count = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).all()
    session.close()
    #Create a dictionary from the row data and append to a list of records
    station_records = []
    for Measurement.station, Measurement.tobs in station_ordered_count:
        station_dict ={}
        station_dict["station"] = Measurement.station
        station_dict["observation count"] = Measurement.tobs
        station_records.append(station_dict)
    #Return the JSON representation of the dictionary
    return jsonify(station_records)

#Create route /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
#Create a link from Python to database
def tobs():
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year of data.
    station_temp_year = session.query(Measurement.station,Measurement.date, Measurement.tobs).\
        filter((Measurement.date >= '2016-08-18'), (Measurement.station == 'USC00519281')).\
        order_by(Measurement.date.desc()).all()
    session.close()
    #Create a dictionary from the row data and append to a list of records
    station_temp_records = []
    for Measurement.station, Measurement.date, Measurement.tobs in station_temp_year:
        station_temp_dict ={}
        station_temp_dict["station"] = Measurement.station
        station_temp_dict["date"] = Measurement.date
        station_temp_dict["temperature obervation"] = Measurement.tobs
        station_temp_records.append(station_temp_dict)
        
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(station_temp_records)

# Create route /api/v1.0/<start> 
@app.route("/api/v1.0/<start>")
#Create a link from Python to database
def start_date(start):
    session = Session(engine)
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_formatted = dateutil.parser.parse(start).strftime("%Y-%m-%d")
    station_temps = session.query(Measurement.station,Measurement.date,
        func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_formatted).\
        group_by(Measurement.date).all()
    session.close()
    return jsonify(station_temps)
    
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# Create route /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
#Create a link from Python to database
def date_range(start, end):
    session = Session(engine)
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    station_date_range = session.query(Measurement.station,Measurement.date,
        func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        group_by(Measurement.date).all()
    session.close()
   #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start 
    return jsonify(station_date_range)

if __name__== "__main__":
    app.run(debug=True)