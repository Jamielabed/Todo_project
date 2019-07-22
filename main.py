import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
import os
import json
from yelpapi import YelpAPI

YELP_API_KEY = "cXFG1vvpqbRy7gQvhqKcbklCku8oq5AhVf5_goxfJ74qz6LcIAqB9fvzx7nZZI92ChAMHJ_02aQ923Q55Zstp8pfKZ4IYDE6iStAkPAF1PtOZkvCQq9Rx-W-hxU2XXYx"



JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/main.html')

class searchResults(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/main.html')
        yelp_api = YelpAPI(YELP_API_KEY)
        results = yelp_api.search_query(location= "Chicago, IL")
        return json.loads(results)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/searchResults', searchResults)
], debug=True)
