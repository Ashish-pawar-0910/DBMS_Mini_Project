from os import curdir
from typing import Text
from flask import *
# from flask.scaffold import _matching_loader_thinks_module_is_package
from werkzeug.utils import redirect
from flask_mysqldb import MySQL #pip install flask_mysqldb
import yaml                     #pip install pyyaml
import MySQLdb.cursors
import re
import inspect
import validators
import requests
from datetime import datetime, date
import time

mydata=yaml.load(open('private.yaml'))
app=Flask(__name__)
app.secret_key = mydata['sec_key']

app.config['MYSQL_HOST']=mydata['mysql_host']
app.config['MYSQL_USER']=mydata['mysql_user']
app.config['MYSQL_PASSWORD']=mydata['mysql_password']
app.config['MYSQL_DB']=mydata['mysql_db']

mysql=MySQL(app)

# create database MiniProject
# create table RegisterStudent
# CREATE TABLE RegisterStudent ( 
#     ParticipantId int NOT NULL AUTO_INCREMENT,
#     fname varchar(20) NOT NULL,  
#     lname varchar(20) NOT NULL,  
#     dept varchar(20) NOT NULL,  
#     division varchar(10) NOT NULL,  
#     rollno varchar(20) NOT NULL, 
#     email varchar(40) NOT NULL,  
#     username varchar(20) NOT NULL,  
#     pswd varchar(20) NOT NULL, 
#     PRIMARY KEY (ParticipantId) 
# )
# CREATE TABLE adminDetails ( 
#     adminuser varchar(20) NOT NULL,  
#     pswrd varchar(20) NOT NULL, 
#     PRIMARY KEY (adminuser) 
# )
# add register method with its updated form in index
# add log in method with its updated form in index
# add logout mrthod and its button in new logged in page
# INSERT INTO RegisterStudent(adminuser, pswrd) VALUES('admin','admin@123');
@app.route('/', methods=['GET','POST'])
def base():
    case=0
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'dept' in request.form and 'div' in request.form and 'rollno' in request.form and 'email' in request.form  and 'username' in request.form and 'password' in request.form :
        student=request.form
        fname=student['fname']
        lname=student['lname']
        dept=student['dept']
        div=student['div']
        rollno=student['rollno']
        email=student['email']
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email})
        status = response.json()['status']
        mails=email.split('@')
        if status == "invalid":
            # flash("Email does not exist. Enter valid email!!")
            return render_template('index.html',case=1)
        elif mails[1]!='pccoepune.org':
            # flash("Enter Official email id only!!")
            return render_template('index.html', case=2)
        username=student['username']
        pswd=student['password']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM RegisterStudent WHERE username = % s', (username, ))
        participant= cur.fetchone()
        
        # users_email=email
        if participant:
            # flash('Account already exists !')
            return render_template('index.html', case=3)
        elif not re.match(r'[A-Za-z0-9]+', username):
            # flash('Username must contain only characters and numbers !') 
            return render_template('index.html', case=4)
        else:
            cur.execute("INSERT INTO RegisterStudent(fname, lname, dept, division, rollno, email, username, pswd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(fname,lname,dept,div,rollno,email,username,pswd))
            mysql.connection.commit()
            # flash('You have successfully registered !')
            return render_template('index.html', case=5)
        redirect('/login')
    elif request.method == 'POST':
        flash('Please fill out the form !')
    case=0
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
        username = request.form['uname']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM RegisterStudent WHERE username = % s AND pswd = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['username']
            print('Logged in successfully !')
            cursor.execute("SELECT * FROM registerEvent ORDER BY edate ASC,eetime ASC;")
            event_data=cursor.fetchall()
            return render_template('user.html', user = account['username'], event_data=event_data)
        else:
            print('Incorrect username / password !')
    return render_template('index.html', msg = msg)

@app.route('/admin-login', methods =['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'admin-uname' in request.form and 'admin-password' in request.form:
        admin_username = request.form['admin-uname']
        admin_password = request.form['admin-password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminDetails WHERE adminuser = % s AND pswrd = % s', (admin_username, admin_password, ))
        admin = cursor.fetchone()
        d=date.today()
        current_date=d.strftime("%d/%m/%Y")
        if admin:
            session['loggedin'] = True
            # session['id'] = admin['id']
            session['adminuser'] = admin['adminuser']
            print('Admin Logged in successfully !')
            cursor.execute("SELECT * FROM registerEvent ORDER BY edate ASC,eetime ASC;")
            event_data=cursor.fetchall()
            return render_template('admin.html',useradmin=admin_username,event_data=event_data)
        else:
            print('Incorrect username / password !')
        
    return render_template('index.html', msg = msg)


# CREATE TABLE registerEvent( 
#     eid varchar(20) NOT NULL,
#     ename varchar(20) NOT NULL,
#     etype varchar(20) NOT NULL,
#     edate DATE NOT NULL,
#     estime TIME NOT NULL,
#     eetime TIME NOT NULL,
#     einfo TEXT NOT NULL,
#     eloc varchar(255) NOT NULL,
#     PRIMARY KEY (eid) 
# );

@app.route('/events', methods = ['GET','POST'])
def create_event():
    if request.method == 'POST':
        event=request.form
        eid=event['event-id']
        ename=event['event-name']
        etype=event['event-type']
        edate=event.get('event-date')
        estime=event.get('event-start-time')
        eetime=event.get('event-end-time')
        einfo=event['event-info']
        eloc=event['event-location']
        # start_time = time.strptime(str(estime),"%Y-%m-%d %H:%M")
        # end_time = time.strptime(str(eetime),"%Y-%m-%d %H:%M")
        # print(etype,edate,estime,eetime)

        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO registerEvent(eid, ename, etype, edate, estime, eetime, einfo, eloc) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(eid, ename, etype, edate, estime, eetime, einfo, eloc))
        mysql.connection.commit()
        # print("event created")
        cur.execute("SELECT * FROM registerEvent ORDER BY edate ASC,eetime ASC;")
        event_data=cur.fetchall()
        return render_template('admin.html',event_data=event_data,flag='success')
    else:
        return render_template('admin.html')

# CREATE TABLE registeredStudents(
#     eid varchar(25), 
#     eventname varchar(30),
#     usermail varchar(80),
#     username varchar(30)
# );

# INSERT INTO registeredStudents(eid,eventname,usermail,username)
#     SELECT re.eid, re.ename, rs.email, rs.username
#     FROM registerEvent re, registerstudent rs
#     WHERE re.eid=event_id and rs.username=session['username']
#     and NOT EXISTS( SELECT usermail FROM registeredstudents rs WHERE rs.eid =event_id and rs.usermail=session['username]);

@app.route('/registerEvent/<event_id>', methods = ['GET','POST'])
def registerEvent(event_id):
    eid=event_id
    if request.method == 'POST':
        current_user=session['username']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO registeredStudents(eid,eventname,usermail,username) SELECT re.eid, re.ename, rs.email, rs.username FROM registerEvent re, registerstudent rs WHERE re.eid=%s and rs.username=%s and NOT EXISTS( SELECT rs.usermail FROM registeredstudents rs,registerEvent re WHERE rs.eid =re.eid and rs.username=%s)",(eid,current_user,current_user))
        print(event_id)
        mysql.connection.commit()
        return render_template('user.html')
    else:
        return redirect('/logout')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    # session.pop('id', None)
    session.pop('username', None)
    print("Logged out!")
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)