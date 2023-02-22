'''
The below 7 lines import all of the modules necessary for the backend and backend/frontend connection. The especially important imports are the json, init, and sqlalchemy imports.
The "import json" import allows for the code in line 53, where the dump records are returned in json format, so that the python objects are readable in JSON format (text format). SQLAlchemy
is the database library being used to store all of the database info for this feature. Finally, the _init_ module is necessary, as it lets the interpreter know that there is Python code in a particular directory. 
In this case, there is Python code in the /api and /model directories.
'''

from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

'''
The below is where the "FactofDay" class is being defined. This contains all of the data for the feature that needs to be managed.
'''
class FactofDay(db.Model):
    __tablename__ = 'FactDay'  
    
    '''
    The below sets all of the keys that are going to be looked at. The id key is special, as it is the primary key. This is what any sort of PUT and DELETE requests will be passed through if operable.
    '''
    id = db.Column(db.Integer, primary_key=True)
    _fact = db.Column(db.String(255), nullable=False)
    _date = db.Column(db.String(255), nullable=False)
    _year = db.Column(db.Integer, nullable=False )
    
    '''
    This is constructing the fact object and the "_init_" portion is initializing the variables within that fact object. 
    In this case, this is the fact, date, and year variables that are within this object.
    '''
    def __init__(self, fact, date, year):
        self._fact = fact
        self._date = date
        self._year = year
    
    '''
    the following lines 44-75 contain the setter and getter methods. each of the three above variables (fact, date, year)
    are being extracted from the object and then updated after the object is created. 
    '''
    @property
    def fact(self):
        return self._fact
    
    # setting fact variable in object

    @fact.setter
    def fact(self, fact):
       self._fact = fact
    
    # extracting date from object
    @property
    def date(self):
        return self._date
    
    # setting date variable in object
    
    @date.setter
    def date(self, date):
       self._date = date
    
    # extracting year from object
    
    @property
    def year(self):
        return self._year
    
    # setting year variable in object
    
    @year.setter
    def year(self, year):
       self._year = year
    
    '''
    The content is being outputted using "str(self)". It is being returned in JSON format, which is a readable format. This is a getter function.
    '''
    def __str__(self):
        return json.dumps(self.read())
    
    
    '''
    defining the create method. self allows us to access all of the attributes 
    of the current object. after the create method is defined, the data is queried from the DB.
    in this case, since it is the create method, the data is being ADDED, and then db.session.commit() is used
    to commit the DB transaction and apply the change to the DB.
    '''
    
    '''
    here, there is an integrity error "except" statement. db.session would be autocommitted 
    without the db.session.remove() line, and that's something we don't want for the purpose of the project.
    '''
    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    '''
    the delete method is defined with the "self" parameter. this method is mainly for certain instances in the DB being 
    garbage collected, and the object kills itself.
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    '''
    read method with the self parameter, reading the object with all of the 
    properties: fact, date, and year are being returned.
    '''
    def read(self):
        return {
            "fact" : self.fact,
            "date" : self.date,
            "year" : self.year,
        }

'''
handling the situation where the table is completely empty,
returns the length from the session query of the initialized class FactofDay to be 0.
''' 
def fact_table_empty():
    return len(db.session.query(FactofDay).all()) == 0

'''
defines the initFactDay function, and then creates the tables and the DB here through the db.create_all() method.
'''
def initFactDay():
    db.create_all()
    #db.init_app(app)
    if not fact_table_empty():
        return
    
    print("Creating test data")
    """Create database and tables"""
    """Tester data for table"""
    
    f1 = FactofDay("Arizona became the 48th state in the Union.", "February 14th", 1912)
    f2 = FactofDay("The USS Maine Sank after an explosion in Havana Harbor", "February 15th", 1898)
    f3 = FactofDay("Power in Cuba was seized by Fidel Castro", "February 16th", 1959)

    
    '''
    the variable "factslist" being used for the tester data, containing f1, f2, 
    and f3, the variables with the sample data above.
    '''
    factslist = [f1, f2, f3]
    
    
    '''
    the below is for the sample data: for each fact in the defined factlist, the DB session will add that fact, and then commit the transaction
    with the next line. or, if there is bad/duplicate data, the data will not be committed, and session will be rolled back to its previous
    state. 
    '''

    for fact in factslist:
        try:
            db.session.add(fact)
            db.session.commit()
        except IntegrityError as e:
            print("Error: " +str(e))
            '''fails with bad or duplicate data'''
            db.session.rollback()    
