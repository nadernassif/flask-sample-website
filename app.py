from flask import (Flask, flash, redirect, render_template,  url_for, abort, request, session)
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(12)

'''database initialization'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)

'''database definition'''
class users(db.Model):


   id = db.Column('id', db.Integer, primary_key = True)
   username = db.Column(db.String(100))
   password = db.Column(db.String(50))
   __tablename__ = 'users'
   __table_args__ = {'extend_existing': True}
   
   def __init__(self, username, password):
      self.username = username
      self.password = password


@app.route('/showall')
def show_all():
   return render_template('show_all.html', users = users.query.all() )

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = users(request.form['username'])
        password = users(request.form['password'])
        if username == users['username'] and password == users['password']:
            
            session['user'] = username
            flash('login successful','info')
            return redirect('/dashboard')
        else:
            flash('wrong password?','error')
            return redirect('/login')
    
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    #if('user' in session and session['user'] == users['username']):
        return render_template("dashboard.html")
    #invalid session or user logged out
    #return '<h1>You are not logged in.</h1>'  


@app.route('/newuser', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['username'] or not request.form['password']:
         flash('Please enter all the fields', 'error')
      else:
         global users 
         users = users(request.form['username'], request.form['password'])
         db.session.add(users)
         db.session.commit()
         flash('Record was successfully added','info')
         return redirect(url_for('login'))
   return render_template('new.html')


@app.route('/logout',methods=['POST'])
def logout():
    if(request.method == 'POST'):
        session.pop('user')         
        session['user'] = False
        return redirect('/login')
    
@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
