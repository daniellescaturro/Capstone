from flask import Flask, jsonify, g
import models
# import requests

DEBUG = True
PORT = 8000

app = Flask(__name__)

# token = 'qtRxFBWCo3VmtnTbf95_TbanMIP_5x0ZjqKiGfLqVj12HnSXjULlBNTWfEh8oA4fUkg3_k7REPYg5HmhmJzae5KEqXfSyMeGrAfRBG5Z93hCR_NSdwxXKqWTKxvFX3Yx'
# headers = {'Authorization': f'Bearer {token}'}
# r = requests.get('https://api.yelp.com/v3/businesses/search?categories=restaurants&categories=bars&location=brooklyn, ny', headers=headers)
# print(r.json())

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def idex():
    return "Hello"

# @app.route('/sayhi/<username>')
# def hello(username):
#     return "Hello {}".format(username)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
