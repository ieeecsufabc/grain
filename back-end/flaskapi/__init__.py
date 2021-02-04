
import flask
from flask import Flask, request, jsonify
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

# Routes
from flaskapi import routes

# Home Route
@app.route('/')
def api_home():
    return "<h1>Grain Count API</h1><p>This site is a prototype API for the grain count project.</p>"

# Headers to fix CORS errors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    # threaded to allow serving to multiple clients at once
    app.run(threaded=True, debug=True)

# Running on different port:
#set FLASK_APP=run.py
#flask run -h localhost -p 3000