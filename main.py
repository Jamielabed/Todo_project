import os
from google.appengine.ext import ndb
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import urlfetch
import os
import json
from Restaurant_models import Restaurant
import yelpapikey


JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():

    return ndb.Key('Parent', 'default_parent')



class Interest(ndb.Model):
    interests = ndb.StringProperty()

def get_restaurant_info(city):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+yelpapikey.YELP_API_KEY}

    result_unformatted = urlfetch.fetch(
        #payload = form_data,
        method=urlfetch.GET,
        url = "https://api.yelp.com/v3/businesses/search?location="+city,
        headers=headers).content
    result = json.loads(result_unformatted)
    return result


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
        possible_interests =["Afghan", "African", "Senegalese"]
        template = JINJA_ENV.get_template('templates/InterestPage.html')
        data = {
            'Interests': Interest.query(ancestor=root_parent()).fetch(),
            'Possible_Interests': possible_interests
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


    def post(self):
        for i in range(1,4):
            added = self.request.get('new_interest'+str(i))
            if(added != ""):
                #go throough all interests in the database
                #and if any match what we are about to add,
                #then don't add it. Otherwise, add it
                new_interest = Interest(parent = root_parent())
                new_interest.interests = added
                existing_interests = Interest.query(Interest.interests == added, ancestor = root_parent()).fetch()
                if(len(existing_interests) == 0):
                    new_interest.put()


        self.response.headers['Content-Type'] = 'text/html'
        self.redirect('/AddInterest')
        print(new_interest)
        print("this is a test line")
        print(added)

class DeleteInterests(webapp2.RequestHandler):
    def post(self):
        to_delete = self.request.get('to_delete', allow_multiple=True)
        for entry in to_delete:
            key = ndb.Key(urlsafe=entry)
            key.delete()
        # redirect to '/' so that the MainPage.get() handler will run and show
        # the list of dogs.
        self.redirect('/AddInterest')


class searchResults(webapp2.RequestHandler):
    def get(self): #for a get request
        query = self.request.get("location")
        self.response.headers['Content-Type'] = 'text/html'
        location = self.request.get('location')
        index_template = JINJA_ENV.get_template('templates/Restaurants.html')
        data = {
            'data': get_restaurant_info(query)
        }
        print data
        self.response.write(index_template.render(data))







class MapsPage(webapp2.RequestHandler):
    API_KEY = "AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
    def get(self):
        currentLocation = json.loads(get_current_location())
        food_types = ["Pizza", "American (New)", "Italian"]
        # returns restaurants that match user preferences
        restaurants_out = filterRestaurants(food_types)
        # adds distance and duration attributes and returns restaurants_out
        restaurants_out = getDistances(restaurants_out)

        user = users.get_current_user()
        template = JINJA_ENV.get_template('templates/main.html')
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
            "restaurants": restaurants_out
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))




def filterRestaurants(user_food_types):
    restaurants = get_restaurant_info("Chicago")
    print "got restaurant info"
    restaurants_out = []
    for num in range(len(restaurants['businesses'])):
        categories = restaurants['businesses'][num]['categories']
        include = False
        for cat_num in range(len(categories)):
            for type in user_food_types:
                if type == categories[cat_num]['title']:
                    include = True
        if include == True:
            print restaurants["businesses"][num]
            restaurants_out.append(restaurants["businesses"][num])
    return restaurants_out

def getDistances(restaurantsList):
    currentLocation = json.loads(get_current_location())
    for restaurant in restaurantsList:
        distMatrix = get_dist_matrix(currentLocation,restaurant)
        restaurant["distance"] = distMatrix['rows'][0]['elements'][0]['distance']['text']
        restaurant["duration"] = distMatrix['rows'][0]['elements'][0]['duration']['text']
        print restaurant['name']
        print restaurant['distance']
        print restaurant['duration']
    return restaurantsList

def get_current_location():
    headers = {'Content-Type': 'application/json'}
    result = urlfetch.fetch(
             url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE",
             method=urlfetch.POST,
             headers=headers)
    return result.content

def get_dist_matrix(curLoc, rest):
    current_latitude = curLoc["location"]["lat"]
    current_longitude = curLoc["location"]["lng"]
    dest_lat = rest['coordinates']['latitude']
    dest_long = rest['coordinates']['longitude']
    distMatrixURL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(current_latitude) + "," + str(current_longitude) + "&destinations=" + str(dest_lat) + "," + str(dest_long) + "&key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
    headers = {'Content-Type': 'application/json'}
    result = urlfetch.fetch(
             url=distMatrixURL,
             method=urlfetch.POST,
             headers=headers)
    return json.loads(result.content)

def sortbyDuration(restaurantsList):
    for restaurant in restaurantsList:
        duration = restaurant['duration']
        duration_int = int(duration.split()[0])

# name = result['businesses'][num]['name']
# categories = result['businesses'][num]['categories'][cat_num]['title']
# latitude = result['businesses'][num]['coordinates']['latitude']
# longitude = result['businesses'][num]['coordinates']['longitude']



class FavoritesPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/favorites.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest',AddInterestPage),
    ('/DeleteInterests', DeleteInterests),
    ('/searchResults', searchResults),
    ('/maps', MapsPage),
    ('/favorites', FavoritesPage)
], debug=True)
