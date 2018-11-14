#Dependencies

import sqlalchemy
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


import datetime as dt
from flask import Flask, jsonify

#----
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
#----
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#----
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        #f"/api/v1.0/<start><br/>"
        #f"/api/v1.0/<start>/<end>"
    )

#----	
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_rain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <="2017-08-23").all()
    precip_box = []
	
    for tobs in one_year:
        prcp_dict = {}
        prcp_dict["date"] = tobs[1]
        prcp_dict["tobs"]=tobs[0]
        prcp.append(precip_box)

    return jsonify(precip_box)

#----	
@app.route("/api/v1.0/stations")
def stations():
    station_avails = session.query(Station.station).all()
    station_name = list(np.ravel(station_avails))

    return jsonify(station_name)

#----
@app.route("/api/v1.0/tobs")
def tobs():
	one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
	
	year_2017 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > year_2017).order_by(Measurement.date).all()
	tobs_list = list(np.ravel(tobs))
	
	return jsonify(tobs_list)

#----
if __name__ == '__main__':
    app.run(debug=True)  