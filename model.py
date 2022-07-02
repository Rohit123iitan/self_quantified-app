from app import db

class User(db.Model):
    __tablename__="registration"
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_name=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
class Tracker(db.Model):
    __tablename__="tracker"
    tracker_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name=db.Column(db.String, unique=True, nullable=False)
    Description=db.Column(db.String)
    Tracker_type=db.Column(db.String)
    settings=db.Column(db.String)
class Logs(db.Model):
    __tablename__="logs"
    logs_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Time=db.Column(db.String, unique=True, nullable=False)
    date=db.Column(db.String)
    Value=db.Column(db.String)
    Tracker_name = db.Column(db.String)
    Notes=db.Column(db.String)
    
from function import *
    