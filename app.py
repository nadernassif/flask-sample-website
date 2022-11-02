from flask import Flask
from flask import (Flask, flash, redirect, render_template, request, session, abort)
import os


app = Flask(__name__)
app.secret_key = os.urandom(12) 

#hardcoded values to be replaced with db values
user = {"username": "nader", "password": "password"}


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:
            
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash('wrong password?')
    
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if('user' in session and session['user'] == user['username']):
        return render_template("dashboard.html")
    #invalid session or user logged out
    return '<h1>You are not logged in.</h1>'  


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
    app.run(debug=True)
