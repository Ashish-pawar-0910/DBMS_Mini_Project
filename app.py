from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import inspect
import validators
import requests

app=Flask(__name__)

@app.route('/')
def base():
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)