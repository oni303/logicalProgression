#!/usr/bin/env python3

from flask import Flask, render_template, flash, request, jsonify, redirect, url_for, send_from_directory
from wtforms import Form, DateField, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import pymysql
import json
import time
import datetime
import sys
import yaml
 

baseUrl = ''
dbServer = ''
dbUser = ''
dbPw = ""
dbName = ""

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'changeME'
 
class ReusableForm(Form):
    date = DateField('date-1', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    if request.method == 'POST':
        date=request.form['date-1']
        print(date)
 
        sessionType = request.form['sessionType']
        duration = request.form['sessionDuration']

        route = 1
        routes = []
        moreRoutes = True
        while moreRoutes:
            r = {}
            try:
                r['grade'] = float(request.form["grade_"+str(route)])
                if r['grade'] <= 2.0: 
                    if request.form["subGrade_"+str(route)] == "Hard":
                        r['grade'] += 0.5
                elif r['grade'] > 2.0: 
                    if request.form["subGrade_"+str(route)] == "Hard":
                        r['grade'] += 1 
                r['holdType'] = request.form["holdType_"+str(route)]
                r['steepness'] = int(request.form["steepness_"+str(route)])
                try:
                    r['sent'] = int(request.form["sent_"+str(route)])
                except KeyError:
                    r['sent'] = 0
                try:
                    r['warmUp'] = int(request.form["warmUp_"+str(route)])
                except KeyError:
                    r['warmUp'] = 0 
                r['tries'] = int(request.form["tries_"+str(route)])
                r['comment'] = request.form["comment_"+str(route)]
                routes.append(r)
                route += 1
            except KeyError:
                moreRoutes = False
        
        idate = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
        session = {'date':idate, 'type':sessionType, 'duration':duration, 'routes':routes}
        r = requests.put(baseUrl + '/session', data = json.dumps(session))
        flash('Saved ' + date)

    return render_template('index.html', form=form)

@app.route('/session', methods=['PUT'])
def addSession():

    db = pymysql.connect(dbServer,dbUser,dbPw,dbName)
    dbc = db.cursor() 
    session = json.loads(request.data.decode())

    dbc.execute("insert into sessions(date,type,climbDuration) values (%s,%s,%s)",(int(session['date']),session['type'],int(session['duration'])))
    dbc.execute('select ID from sessions where date=%s', (str(session['date']),))
    dbSessions = dbc.fetchone()[0]
    print(session)
    for route in session['routes']:
        print(route['comment'])
        dbc.execute("insert into boulder(sessionID,grade,tries,sent,warmUp,steepness,holdType,comment) values (%s,%s,%s,%s,%s,%s,%s,%s)",(int(dbSessions), float(route['grade']), int(route['tries']), str(route['sent']), str(route['warmUp']), int(route['steepness']), str(route['holdType']), str(route['comment'])))
    db.commit()
    #except :
    #    print(sys.exc_info()[0] )
    #    db.rollback()
    db.close()
    

    return json.dumps({'state':"OK"})
 
if __name__ == "__main__":
    global baseUrl 
    global dbServer 
    global dbUser 
    global dbPw 
    global dbName 
    with open("example.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
        baseUrl = config['baseUrl'] 
        dbServer = config['dbServer'] 
        dbUser = config['dbuser'] 
        dbPw = config['dbPw']
        dbName = config['dbName']

        app.run()
    except yaml.YAMLError as exc:
        print("ERROR: not able to load config")
        sys.exit(-1)
