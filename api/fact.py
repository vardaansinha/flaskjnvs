from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
# the class FactofDay, defined in the corresponding model file for the feature, is being imported for its usage in the api.
from model.facts import FactofDay

# this is where the blueprint class is defined and the url prefix is set, which is then registered to the app in the main.py file.
fact_api = Blueprint('fact_api', __name__, url_prefix='/api/fact')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(fact_api)

# this is the main entry point for the app, with the class factAPI. 
class factAPI:
    # the _create class is being referred to for the post method, to post the objects.        
    class _Create(Resource):
        def post(self):
             ''' Read data for json body '''
             body = request.json
             
             ''' Avoid garbage in, error checking '''
            # validate name
            
            # here, this handles error checking, as the shortest fact in the world is 13 characters, so if the fact is less than that, it is deemed invalid and not added to the DB.
             fact = body.get('fact')
             if fact is None or len(fact) < 13:
                return {'message': f'Fact is missing'}, 210
           
            # look for date, year variables
             date = body.get('date')
             year = body.get('year')


             # this sets up the fact object
             uo = FactofDay(fact, date, year)
           
           
             # this adds the fact to the DB (uo.create())
             fact = uo.create()
             
             # if the addition was successful, then the fact is returned to the user in a readable JSON format.
             if fact:
                return jsonify(fact.read())
            # failure returns error
             return {'message': f'Processed fact error'}, 210
    
    # _Read class, needed for the GET request.     
    class _Read(Resource):
        def get(self):
            facts = FactofDay.query.all()    # read/extract all facts from database
            json_ready = [fact.read() for fact in facts]  # prepares the readable output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        


    # building the API endpoints. there is a create and read endpoint, to serve for both the GET and POST requests.
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
