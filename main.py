import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries
from flask_cors import CORS

# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from model.nflteam import initNFLTeams
from model.scores import initCool
from model.facts import initFactDay
from model.breakingnews import initBreakingNews

# setup APIs
from api.nflteam import nflteam_api # Blueprint import api definition
from api.score import score_api # Blueprint import api definition
from api.fact import fact_api
from api.news import breakingnews_api # Blueprint import api definition

# register URIs
app.register_blueprint(nflteam_api) # register app pages
app.register_blueprint(score_api)
app.register_blueprint(fact_api)
app.register_blueprint(breakingnews_api) # register api routes


@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')  
def index():
    return render_template("index.html")

@app.route('/nflteams')  
def nflteams():
    return render_template("nflstat.html")

# just a little fun wrinkle for the backend, where the facts can be updated on the flask server as well in a readable format.
@app.route('/facts')  
def facts():
    return render_template("facts.html")


# this registers all of the functions.
@app.before_first_request
def activate_job():
    #initNFLTeams()
    initCool()
    initFactDay()
    initBreakingNews()


# this runs the application on the development server, for any tester data, etc.
if __name__ == "__main__":
    cors = CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volumes/sqlite.db'
    app.run(debug=True, host="0.0.0.0", port="8679")
    #initNFLTeams()
    initFactDay()
