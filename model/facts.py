from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class FactofDay(db.Model):
    __tablename__ = 'FactDay'  
    
    id = db.Column(db.Integer, primary_key=True)
    _fact = db.Column(db.String(255), nullable=False)
    _date = db.Column(db.String(255), nullable=False)
    _year = db.Column(db.Integer, nullable=False )
    
    def __init__(self, fact, date, year):
        self._fact = fact
        self._date = date
        self._year = year
        
    @property
    def fact(self):
        return self._fact
    
    @fact.setter
    def fact(self, fact):
       self._fact = fact
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date):
       self._date = date
    
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, year):
       self._year = year
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    def read(self):
        return {
            "fact" : self.fact,
            "date" : self.date,
            "year" : self.year,
        }
        
def fact_table_empty():
    return len(db.session.query(FactofDay).all()) == 0

def initFactDay():
    db.create_all()
    db.init_app(app)
    if not fact_table_empty():
        return
    
    print("Creating test data")
    """Create database and tables"""
    """Tester data for table"""
    
    f1 = FactofDay("Arizona became the 48th state in the Union.", "February 14th", 1912)
    f2 = FactofDay("The USS Maine Sank after an explosion in Havana Harbor", "February 15th", 1898)
    f3 = FactofDay("Power in Cuba was seized by Fidel Castro", "February 16th", 1959)
    f4 = FactofDay("Shaurya achieved genius status", "February 17th", 2023)

    
    factslist = [f1, f2, f3]
    

    for fact in factslist:
        try:
            db.session.add(fact)
            db.session.commit()
        except IntegrityError as e:
            print("Error: " +str(e))
            '''fails with bad or duplicate data'''
            db.session.rollback()

initFactDay()
    
