import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():

    return ndb.Key('Parent', 'default_parent')



class Interest(ndb.Model):
    interests = ndb.StringProperty()

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
        data = {
        'Interests': Interest.query(ancestor=root_parent()).fetch()
        }


        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
        print('fine')
    def post(self):

        template = JINJA_ENV.get_template('templates/InterestPage.html')
        # data = {
        # 'Interests': Interest.query(ancestor=root_parent()).fetch(),
        # 'AddInterest':  Interest.query(ancestor=root_parent()).fetch()
        # }
        # print(data['Interests'])
        # new_food = Interest(parent=root_parent())
        # print(new_food)
        # new_food.name = self.request.get('new_intrest')
        # print(new_food.name)
        # data['Interests'].append(new_food)
        # print(data['Interests'])
        new_interest = Interest(parent = root_parent())
        added = self.request.get('new_interest')
        new_interest.interests = added
        new_interest.put()
        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/AddInterest')
        print(new_interest)

class DeleteInterests(webapp2.RequestHandler):
    def post(self):
        to_delete = self.request.get('to_delete', allow_multiple=True)
        for entry in to_delete:
            key = ndb.Key(urlsafe=entry)
            key.delete()
        # redirect to '/' so that the MainPage.get() handler will run and show
        # the list of dogs.
        self.redirect('/AddInterest')



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest', AddInterestPage),
    ('/DeleteInterests', DeleteInterests)
], debug=True)
