from flask import Flask,render_template,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import matplotlib.pyplot as plt
import bcrypt
app=Flask(__name__)
app.secret_key='this is a secret key'
app.permanent_session_Slifetime = timedelta(minutes=50)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///abc_database.sqlite3"
db = SQLAlchemy(app)
from controller import *
from function import *
if __name__=="__main__":
    app.run(debug=True)