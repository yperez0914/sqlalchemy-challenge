# Import Dependencies
# YOUR CODE HERE
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

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
def stations():
    session = Session(engine)

# Return a JSON list of stations from the dataset.



# /api/v1.0/tobs


# Query the dates and temperature observations of the most active station for the last year of data.


# Return a JSON list of temperature observations (TOBS) for the previous year.




# /api/v1.0/<start> and /api/v1.0/<start>/<end>


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

if __name__== "__main__":
    app.run(debug=True)