import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Mes = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (f"<b>Welcome to the Weather API</b></br>"
            f"</br>"
            f"precipitation info: /api/v1.0/precipitation<br>"
            f"station info: /api/v1.0/stations</br>"
            f"temperature observation info: /api/v1.0/tobs</br>"
    )



# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for prcp page...")
    recent = session.query(Mes.date).order_by(Mes.date.desc()).limit(1)
#print(f"The most recent date is: {recent}")
    for row in recent:
        string_date = row[0]
    print(string_date)
    datetime_object = datetime.strptime(string_date, '%Y-%m-%d')
# Calculate the date one year from the last date in data set.
    last_year = datetime_object - dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame and set the index to the date column
    query = session.query(Mes.date, Mes.prcp).filter(Mes.date >= (last_year - dt.timedelta(days=1))).\
        filter(Mes.date <= datetime_object).\
        order_by(Mes.date).all()
    json_return = jsonify(query)
    
    return json_return

@app.route("/api/v1.0/stations")
def stations():
    station = []
    for stat in session.query(Station.station).distinct():
        station.append(stat)
    list_return = jsonify(station)
    return list_return

@app.route("/api/v1.0/tobs")
def tobs():
    
    upside_down = session.query(Mes.station, func.count(Mes.station)).group_by(Mes.station).order_by((func.count(Mes.station).asc())).all()
    for k,v in upside_down:
        most_active = k

    most_active_q = session.query(Mes.date, Mes.tobs).filter(Mes.station == most_active).all()
    most_active_json = jsonify(most_active_q)
    return most_active_json
    


if __name__ == "__main__":
    app.run(debug=True)




