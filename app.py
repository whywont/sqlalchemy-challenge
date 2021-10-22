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
            f"temperature with date: /api/v1.0/YYYY-MM-DD date format</br>"
            f"temperature with start and end date: /api/v1.0/api/v1.0/YYYY-MM-DD/YYYY-MM-DD</br>"
    )



# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
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
        filter(Mes.date <= datetime_object).all()
    
    q_list = []
    #json_return = jsonify(query)
    for date, prcp in query:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        q_list.append(prcp_dict)
        
    
    return jsonify(q_list)
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    station = []
    for stat in session.query(Station.station).distinct():
        station.append(stat)
    list_return = jsonify(station)
   
    session.close()
    return list_return

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    upside_down = session.query(Mes.station, func.count(Mes.station)).group_by(Mes.station).order_by((func.count(Mes.station).asc())).all()
    for k,v in upside_down:
        most_active = k

    most_active_q = session.query(Mes.date, Mes.tobs).filter(Mes.station == most_active).all()
    
    session.close()
    
    all_tobs = []
    for date, tobs in most_active_q:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_api(start):
    
    session = Session(engine)
    
    start_date = session.query(func.min(Mes.tobs), func.avg(Mes.tobs), func.max(Mes.tobs)).filter(Mes.date >=start).all()
    
    
    session.close()
    
    start_list = []
    for mini, avg, maxi in start_date:
        start_tobs = {}
        start_tobs['min temp'] = mini
        start_tobs['avg temp'] = avg
        start_tobs['max temp'] = maxi
        start_list.append(start_tobs)
        
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_api(start, end):
    
    session = Session(engine)
    
    start_date = session.query(func.min(Mes.tobs), func.avg(Mes.tobs), func.max(Mes.tobs)).filter(Mes.date >=start).\
                        filter(Mes.date<= end).all()
    
    start_list = []
    for mini, avg, maxi in start_date:
        start_tobs = {}
        start_tobs['min temp'] = mini
        start_tobs['avg temp'] = avg
        start_tobs['max temp'] = maxi
        start_list.append(start_tobs)
    
    session.close()
    return jsonify(start_list)
    

if __name__ == "__main__":
    app.run(debug=True)




