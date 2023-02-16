from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from model.nflteam import NFLTeam

nflteam_api = Blueprint('nflteam_api', __name__, url_prefix='/api/nflteam')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(nflteam_api)

class nflteamAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            team = body.get('teams')
            if team is None or len(team) < 2:
                return {'message': f'Team is missing, or is less than 2 characters'}, 210
            
            # look for score, type
            score = body.get('score')
            type = body.get('type')
            #day = body.get('day')
            # validate uid
            #uid = body.get('id')
            #if uid is None or len(uid) < 2:
            #    return {'message': f'ID is missing, or is less than 2 characters'}, 210
            #''' #1: Key code block, setup USER OBJECT '''
            
            uo = nflteam(teams=team, score=score, type=type)
            
            ''' Additional garbage error checking '''
            
            # create nfl news in database
            nflteam = uo.create()
            # success returns json of nfl news
            if nflteam:
                return jsonify(nflteam.read())
            # failure returns error
            return {'message': f'Processed news error'}, 210

    class _Read(Resource):
        def get(self):
            teamname = request.args.get("name", default="all")
            print(teamname)

            if teamname == "all":
                teams = NFLTeam.query.all()    # read/extract all users from database
                json_ready = [team.read() for team in teams]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
            else:
                team = NFLTeam.getTeam(teamname)
                #json_ready = [team.read()]
                return jsonify(team.read())
            

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')