from os import curdir
from flask import *
# from flask.scaffold import _matching_loader_thinks_module_is_package
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import yaml
import requests
import MySQLdb.cursors
import re

# sensitive=yaml.load(open('db_m.yaml'))
# app=Flask(__name__)
# app.secret_key = sensitive['sec_key']


# app.config['MYSQL_HOST']=sensitive['mysql_host']
# app.config['MYSQL_USER']=sensitive['mysql_user']
# app.config['MYSQL_PASSWORD']=sensitive['mysql_password']
# app.config['MYSQL_DB']=sensitive['mysql_db']

mysql=MySQL(app)

# users_email=''
@app.route('/', methods=['GET','POST'])
def index():
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
        cur.execute('SELECT * FROM RegisterUsers WHERE username = % s', (username, ))
        participant= cur.fetchone()
        
        # users_email=email
        if participant:
            # flash('Account already exists !')
            return render_template('index.html', case=3)
        elif not re.match(r'[A-Za-z0-9]+', username):
            # flash('Username must contain only characters and numbers !') 
            return render_template('index.html', case=4)
        else:
            cur.execute("INSERT INTO RegisterUsers(fname, lname, dept, division, rollno, email, username, pswd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(fname,lname,dept,div,rollno,email,username,pswd))
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
        cursor.execute('SELECT * FROM RegisterUsers WHERE username = % s AND pswd = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['username']
            print('Logged in successfully !')
            return render_template('index.html', msg = msg)
        else:
            print('Incorrect username / password !')
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    # session.pop('id', None)
    session.pop('username', None)
    print("Logged out!")
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
