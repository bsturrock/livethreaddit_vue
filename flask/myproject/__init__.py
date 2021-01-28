from flask import Flask
import os
import sys
from flask_cors import CORS
import praw
sys.path.append('../')

CLIENT_ID = '2XmDNj0gkoQZZw'
CLIENT_SECRET = 'Qcs6RiZOpcWWjGK6-2yeZt5Fa5LPgQ'
REDIRECT_URI = 'http://localhost:5000/authorize_callback'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

redd = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=REDIRECT_URI,
                     user_agent="livethreaddit by /u/iamjohnmiller")

