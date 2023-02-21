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
             if fact is None or len(fact) < 2:
                return {'message': f'Fact is missing, or is less than 2 characters'}, 210
           
            # look for date, year
             date = body.get('date')
             year = body.get('year')


           
             uo = FactofDay(fact, date, year)
           
             ''' Additional garbage error checking '''
           
           
             fact = uo.create()
           
             if fact:
                return jsonify(fact.read())
            # failure returns error
             return {'message': f'Processed news error'}, 210
        def put(self):
            parser = reqparse.RequestParser()
            parser.add_argument("fact", required=True, type=str)
            parser.add_argument("date", required=True, type=str)
            parser.add_argument("year", required=True, type=int)
            args = parser.parse_args()

            try:
                fact = db.session.query(FactofDay).get(args["a"])
                if fact:
                    db.session.commit()
                else:
                    return {"message": "fact not found"}, 404
            except Exception as e:
                db.session.rollback()
                return {"message": f"server error: {e}"}, 500

        def delete(self):
            parser = reqparse.RequestParser()
            parser.add_argument("fact", required=True, type=str)
            args = parser.parse_args()

            try:
                fact = db.session.query(FactofDay).get(args["a"])
                if fact:
                    db.session.delete(fact)
                    db.session.commit()
                    return fact.to_dict()
                else:
                    return {"message": "subscription not found"}, 404
            except Exception as e:
                db.session.rollback()
                return {"message": f"server error: {e}"}, 500



    class _Read(Resource):
        def get(self):
            facts = FactofDay.query.all()    # read/extract all users from database
            json_ready = [fact.read() for fact in facts]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
