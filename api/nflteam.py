from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from model.nflteam import NFLTeam

nflteam_api = Blueprint('nflteam_api', __name__, url_prefix='/api/nflteam')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(nflteam_api)

class nflteamAPI:        
    # Create
    class _Create(Resource):
        # Post Method
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            team = body.get('team')
            pointsfor = body.get('pointsfor')
            pointsagainst = body.get('pointsagainst')
            playoffs = body.get('playoffs')
            gameswonaway = body.get('gameswonaway')
            gameswonathome = body.get('gameswonathome')
            gameswon = body.get('gameswon')
            gamesplayedaway = body.get('gamesplayedaway')
            gamesplayedathome = body.get('gamesplayedathome')
            gamesplayed = body.get('gamesplayed')
            gameslostaway = body.get('gameslostaway')
            gameslostathome = body.get('gameslostathome')
            gameslost = body.get('gameslost')
            gamesdrawn = body.get('gamesdrawn')
            division = body.get('division')
            
            teamObj = NFLTeam(division=division, team=team, gamesplayed=gamesplayed, gameswon=gameswon, gameslost=gameslost, gamesdrawn=gamesdrawn, gamesplayedathome=gamesplayedathome, gamesplayedaway=gamesplayedaway, gameswonathome=gameswonathome, gameslostathome=gameslostathome, gameswonaway=gameswonaway, gameslostaway=gameslostaway, gamesplayed5=0, gameswon5=0, gameslost5=0, pointsfor=pointsfor, pointsagainst=pointsagainst,  playoffs=playoffs)
            
            ''' Additional garbage error checking '''
            
            # create nfl news in database
            nflteam = teamObj.create()
            # success returns json of nfl news
            if nflteam:
                return jsonify(nflteam.read())
            # failure returns error
            return {'message': f'NFL Team not created'}, 210

    
    # Update
    class _Update(Resource):
        # Put Method
        def put(self):
            ''' Read data for json body '''
            body = request.get_json()
            print(body)
            
            team = body.get('team')
            pointsfor = body.get('pointsfor')
            pointsagainst = body.get('pointsagainst')
            playoffs = body.get('playoffs')
            gameswonaway = body.get('gameswonaway')
            gameswonathome = body.get('gameswonathome')
            gameswon = body.get('gameswon')
            gamesplayedaway = body.get('gamesplayedaway')
            gamesplayedathome = body.get('gamesplayedathome')
            gamesplayed = body.get('gamesplayed')
            gameslostaway = body.get('gameslostaway')
            gameslostathome = body.get('gameslostathome')
            gameslost = body.get('gameslost')
            gamesdrawn = body.get('gamesdrawn')
            division = body.get('division')
            id = body.get('id')
            
            teamObj = NFLTeam(division=division, team=team, gamesplayed=gamesplayed, gameswon=gameswon, gameslost=gameslost, gamesdrawn=gamesdrawn, gamesplayedathome=gamesplayedathome, gamesplayedaway=gamesplayedaway, gameswonathome=gameswonathome, gameslostathome=gameslostathome, gameswonaway=gameswonaway, gameslostaway=gameslostaway, gamesplayed5=0, gameswon5=0, gameslost5=0, pointsfor=pointsfor, pointsagainst=pointsagainst,  playoffs=playoffs)
            
            ''' Additional garbage error checking '''
            
            # create nfl news in database
            nflteam = teamObj.update(id)
            # success returns json of nfl news
            if nflteam:
                return jsonify(nflteam.read())
            # failure returns error
            return {'message': f'NFL Team not created'}, 210

    
    # Read
    class _Read(Resource):
        # Get Method
        def get(self):
            teamname = request.args.get("name", default="all")
            print(teamname)

            if teamname == "all":
                teams = NFLTeam.query.all()    # read/extract all users from database
                json_ready = [team.read() for team in teams]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
            else:
                team = NFLTeam.getTeam(teamname)

                if (team is None):
                    return {'message': f'NFL Team with name: ('+teamname+') not found.'}, 210
                #json_ready = [team.read()]
                return jsonify(team.read())
    
    # Delete
    class _Delete(Resource):
        # Delete Method
        def delete(self):
            teamid = request.args.get("id")
            print(teamid)

            if teamid == "":
                 return {'message': f'NFL Team ID not provided.'}, 210
            else:
                team = NFLTeam.getTeamById(teamid)

                if (team is None):
                    return {'message': f'NFL Team with ID: ('+teamid+') not found.'}, 210
                
                teamName = team._team
                print("deleting nfl team " + team._team)
                
                #json_ready = [team.read()]
                NFLTeam.delete(team)
                return {'message': f'NFL Team \''+teamName+'\' ('+teamid+') deleted.'}, 200
            

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Delete, '/delete')
    api.add_resource(_Update, '/update')
    api.add_resource(_Read, '/')