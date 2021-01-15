# sqlalchemy-challenge
# SQL-Challenge
<br>
For this project, I used SQLAlchemy ORM queries, Pandas, and Matplotlib for climate analysis in Hawaii!
<br>

# Climate Analysis and Exploration
<br>
Using the data provided from the hawaii.sqlite files, I was able to perform a precipitation analysis to pull the temperature observation data from the most active weather station in Hawaii by creating an engine using SQLAlchemy and performing queries for detailed analysis.
<br>

## Example:

```
engine = create_engine("sqlite:///hawaii.sqlite", echo = False)Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
session.query(Measurement.date).order_by(Measurement.date.desc()).first()
query_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
results = session.query(Measurement.date, Measurement.prcp).\
    filter(func.strftime(Measurement.date >= query_date)).all()
results
````

<br>
Then, I loaded the Pandas DataFrame and plotted the results.
<br>

Plot of Precipitation:
[Hawaii Precipitation Results](https://github.com/yperez0914/sqlalchemy-challenge/blob/main/precipitation.png)
Histogram of Most Active Station's Temperature Observations:
[Most Active Station's Temperature Observations](https://github.com/yperez0914/sqlalchemy-challenge/blob/main/Active_Station_Temp.png)
<br>
Find the full dode here: <br>
[Precipitation Queries full code](https://github.com/yperez0914/sqlalchemy-challenge/blob/main/HI_Climate.ipynb)
<br>

<br>
# Climate Analysis and Exploration
<br>

I also performed several queries on the most active station. Ultimately, designing a Flask API using queries.
<br>

## Example: 

```
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
````

<br>
[Flask API full code](https://github.com/yperez0914/sqlalchemy-challenge/blob/main/app.py)
<br>
