import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from model.nflteam import initNFLTeams
from model.scores import initCool
from model.facts import initFactDay

# setup APIs
from api.nflteam import nflteam_api # Blueprint import api definition
from api.score import score_api # Blueprint import api definition
from api.fact import fact_api

# register URIs
app.register_blueprint(nflteam_api) # register app pages
app.register_blueprint(score_api)
app.register_blueprint(fact_api)


@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')  
def index():
    return render_template("index.html")

@app.route('/nflteams')  
def nflteams():
    return render_template("nflstat.html")

@app.route('/facts')  
def facts():
    return render_template("facts.html")



@app.before_first_request
def activate_job():
    initNFLTeams()
    initCool()
    initFactDay()


# this runs the application on the development server
if __name__ == "__main__":
     from flask_cors import CORS
     cors = CORS(app)
     app.run(debug=True, host="0.0.0.0", port="8086")
    #initNFLTeams()
    #initFactDay()
