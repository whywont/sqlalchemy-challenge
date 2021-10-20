# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return("precipitation info: /api/v1.0/precipitation)
    return("station info: /api/v1.0/stations)
    return("temperature observation info: /api/v1.0/tobs)


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

@app.route("/api/v1.0/stations")
def precipitation():
    
@app.route("/api/v1.0/tobs")
def precipitation():
    
if __name__ == "__main__":
    app.run(debug=True)
