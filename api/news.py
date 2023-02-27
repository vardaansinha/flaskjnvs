'''
Breaking News API module. This module handles the create, read, delete and requests from remote clients. The below lines imports libraries 
such as Blueprint, Request, JSON, Resource and Datetime used in the module. Also import Breaking Newd model utils.
'''

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime

from model.breakingnews import BreakingNews
from model.breakingnews import deleteBreakingNews

breakingnews_api = Blueprint('breakingnews_api', __name__,
                   url_prefix='/api/breakingnews')

'''
Referece to the Breaking News Api object
'''
api = Api(breakingnews_api)

'''
This class defines the Breaking News API that handles the create, read, delete and requests from remote clients.
'''
class BreakingNewsAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' 
            Breaking news title  error checking to avoid garbage input. Return error message if input is not correct 
            '''

            title = body.get('title')
            if title is None or len(title) < 2:
                return {'message': f'Title is missing, or is less than 2 characters'}, 210

            ''' 
            Breaking news network  error checking to avoid garbage input. Return error message if input is not correct 
            '''

            network = body.get('network')
            if network is None or len(network) < 2:
                return {'message': f'Network is missing, or is less than 2 characters'}, 210
            
            # Fetch the day news created
            day = body.get('day')

            ''' 
            Create Breaking News instance with title and network params 
            '''
            uo = BreakingNews(title=title, 
                      network=network)
            
            ''' 
            Breaking news day  error checking to avoid garbage input. Return error message if input is not correct 
            '''
            
            if day is not None:
                try:
                    uo.day = datetime.strptime(day, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date of birth format error {day}, must be mm-dd-yyyy'}, 210
            
            ''' 
            Breaking news create object. Return error message if creation is failed 
            '''            
            news = uo.create()
            # success returns json of news
            if news:
                return jsonify(news.read())
            # failure returns error
            return {'message': f'Processed {title}, either a format error or News ID {network} is duplicate'}, 210

    '''
      The Breaking News read method to fetch all the news data from the model. The return is jsonify Flask response object
    '''
    class _Read(Resource):
        def get(self):
            news = BreakingNews.query.all()    # read/extract all news from database
            json_ready = [user.read() for user in news]  # prepare output in json
            return jsonify(json_ready)  

    '''
      The Breaking News delete method to delete news data from the model based on the news item it. The return is jsonify Flask response object message
    '''          
    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            id = body.get('id')
            #print("Deleting Breaking News Item: " + id)        
            deleteBreakingNews(id)
            return f"Has been deleted"

    '''      
     The below is building RESTapi endpoint resource for breaking news 
    '''
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')
