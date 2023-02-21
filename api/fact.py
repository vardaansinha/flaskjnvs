from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from model.facts import FactofDay
from __init__ import db


fact_api = Blueprint('fact_api', __name__, url_prefix='/api/fact')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(fact_api)


class factAPI:        
    class _Create(Resource):
        def post(self):
             ''' Read data for json body '''
             body = request.json
             
             ''' Avoid garbage in, error checking '''
            # validate name
             fact = body.get('fact')
             if fact is None or len(fact) < 13:
                return {'message': f'Fact is missing'}, 210
           
            # look for date, year
             date = body.get('date')
             year = body.get('year')


           
             uo = FactofDay(fact, date, year)
           
             ''' Additional garbage error checking '''
           
           
             fact = uo.create()
           
             if fact:
                return jsonify(fact.read())
            # failure returns error
             return {'message': f'Processed fact error'}, 210
        
    class _Read(Resource):
        def get(self):
            facts = FactofDay.query.all()    # read/extract all users from database
            json_ready = [fact.read() for fact in facts]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
