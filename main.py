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
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('templates/main.html')
        data = {
                 'user': user,
                 'login_url': users.create_login_url(self.request.uri),
                 'logout_url': users.create_logout_url(self.request.uri),
                }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class AddInterestPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/InterestPage.html')
        data = { }


        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest',AddInterestPage)
], debug=True)
