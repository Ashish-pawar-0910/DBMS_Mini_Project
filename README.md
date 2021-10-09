# DBMS_Mini_Project

## ***Event Management System***

Make sure you have the dependencies installed:

1. [git](https://git-scm.com/downloads)
2. [python](https://www.python.org/)

## Built With
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MySQL](https://www.mysql.com/)
- [Bootstrap](https://getbootstrap.com/)

## Prerequisites

Following packages needed to be installed before getiing started with it.
- flask_mysqldb
   pip install flask_mysqldb
- yaml
   pip install pyyaml
- requests
   pip install requests

Start with Website:

1. After cloning repository in your local machine, change directory to `/DBMS_MINI_PROJECT`.
2. To set up your MySQL server credentials change directory to `/private.yaml` file and change foloeing values:
 - `mysql_user`: your username for MySQL
 - `mysql_password`: your password for MySQL
 - `mysql_db`: databse name which you created for this project
 - `sec_key`: secret key for login sessions
    *To get sec_key in python compiler import `import os` and run `os.random(24)`*
    You are all set to run the website.
3. Now run `app.py` file by running `python app.py` or `flask run` in terminal under `/DBMS_MINI_PROJECT` directory. This will give you the path for localhost on which your file is currently running locally. 
4. Paste the path copied from terminal in the browser.
That's it!!
