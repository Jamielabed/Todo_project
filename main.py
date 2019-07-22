import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
import os
import json
from yelp.client import Client

YELP_API_KEY = "cXFG1vvpqbRy7gQvhqKcbklCku8oq5AhVf5_goxfJ74qz6LcIAqB9fvzx7nZZI92ChAMHJ_02aQ923Q55Zstp8pfKZ4IYDE6iStAkPAF1PtOZkvCQq9Rx-W-hxU2XXYx"

client = Client(YELP_API_KEY)

business_response = client.business.get_by_id('yelp-san-francisco')

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/main.html')

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
