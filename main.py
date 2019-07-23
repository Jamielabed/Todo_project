import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
import os
import json

YELP_API_KEY = "cXFG1vvpqbRy7gQvhqKcbklCku8oq5AhVf5_goxfJ74qz6LcIAqB9fvzx7nZZI92ChAMHJ_02aQ923Q55Zstp8pfKZ4IYDE6iStAkPAF1PtOZkvCQq9Rx-W-hxU2XXYx"



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


class searchResults(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/main.html')
        try:
            #form_data = {'location': 'Chicago'}
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer '+YELP_API_KEY}

            result = urlfetch.fetch(
                #payload = form_data,
                method=urlfetch.GET,
                url = "https://api.yelp.com/v3/businesses/search?location=Chicago",
                headers=headers)

            self.response.write(result.content)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')


def get_current_location():
    print "in current location"
    #def post(self):
    print "in post"
    headers = {'Content-Type': 'application/json'}
    result = urlfetch.fetch(
             url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE",
             method=urlfetch.POST,
             headers=headers)
    return result.content
def get_dist_matrix(curLoc, rest):
    latitude = curLoc["location"]["lat"]
    longitude = curLoc["location"]["lng"]
    distMatrixURL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(latitude) + "," + str(longitude) + "&destinations=" + rest["name"] + "&key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
    headers = {'Content-Type': 'application/json'}
    result = urlfetch.fetch(
             url=distMatrixURL,
             method=urlfetch.POST,
             headers=headers)
    return json.loads(result.content)

class MapsPage(webapp2.RequestHandler):
    API_KEY = "AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
    def get(self):
        #currentLocation = get_current_location()
        currentLocation = json.loads(get_current_location())
        #self.response.write(currentLocation)
        print "in get"

        chicago = {
            "name": "Chicago"
        }
        seattle = {
            "name": "Seattle"
        }
        restaurantsList = [chicago, seattle]
        for restaurant in restaurantsList:
            # separate words in destination should be separated w + (San+Francisco) --> not implemented, see if affects output
            # ^^ put into lat/long so shouldn't be an issue
            distMatrix = get_dist_matrix(currentLocation,restaurant)
            restaurant["distance"] = distMatrix['rows'][0]['elements'][0]['distance']['text']
            restaurant["duration"] = distMatrix['rows'][0]['elements'][0]['duration']['text']
            print restaurant
            print restaurant['duration']

class FavoritesPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/InterestPage.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest',AddInterestPage),
    ('/searchResults', searchResults),
    ('/maps', MapsPage),
    ('/favorites', FavoritesPage)
], debug=True)
