import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users

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
