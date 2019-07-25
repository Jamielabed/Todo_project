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
import googleapikey


JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def root_parent():

    return ndb.Key('Parent', 'default_parent')

# database for FOOD TYPES
class Interest(ndb.Model):
    interests = ndb.StringProperty()

# database for RESTURANTS
class RestaurantInterest(ndb.Model):
    rest_int = ndb.StringProperty()

def get_restaurant_info(lat,long):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+yelpapikey.YELP_API_KEY}

    result_unformatted = urlfetch.fetch(
        #payload = form_data,
        method=urlfetch.GET,
        url = "https://api.yelp.com/v3/businesses/search?latitude="+str(lat)+"&longitude="+str(long)+"&limit=50",
        headers=headers).content
    result = json.loads(result_unformatted)


    return result


def get_interests_list():
    existing_interests = Interest.query(ancestor = root_parent()).fetch()
    interests_list = []
    for interest in existing_interests:
        interests_list.append(interest.interests)
    return interests_list




# this will be the insterest list for RESTURANTS
def get_restaurant_list():
    current_interests = RestaurantInterest.query(ancestor = root_parent()).fetch()
    RestaurantInterests_list = []
    for rest_int in current_interests:
        RestaurantInterests_list.append(rest_int.rest_int)
    return RestaurantInterests_list



class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('templates/main.html')

        data = {
                 'user': user,
                 'login_url': users.create_login_url('/AddInterest'),
                 'logout_url': users.create_logout_url(self.request.uri),
                 "api_key": googleapikey.GOOGLE_API_KEY
                }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))




possible_interests =["Afghan ",
"African ",
"Senegalese ",
"South African ",
"American (New) ",
"American  ",
"Arabian ",
"Argentine ",
"Armenian ",
"Asian Fusion ",
"Australian ",
"Austrian ",
"Bangladeshi ",
"Barbeque ",
"Basque ",
"Belgian ",
"Brasseries ",
"Brazilian ",
"Breakfast & Brunch ",
"Pancakes ",
"British ",
"Buffets ",
"Bulgarian ",
"Burgers ",
"Burmese ",
"Cafes ",
"Themed Cafes ",
"Cafeteria ",
"Cajun/Creole ",
"Cambodian ",
"Caribbean ",
"Dominican ",
"Haitian ",
"Puerto Rican ",
"Trinidadian ",
"Catalan ",
"Cheesesteaks ",
"Chicken Shop ",
"Chicken Wings ",
"Chinese ",
"Cantonese ",
"Dim Sum ",
"Hainan ",
"Shanghainese ",
"Szechuan ",
"Comfort Food ",
"Creperies ",
"Cuban ",
"Czech ",
"Delis ",
"Diners ",
"Dinner Theater ",
"Eritrean ",
"Ethiopian ",
"Fast Food ",
"Filipino ",
"Fish & Chips ",
"Fondue ",
"Food Court ",
"Food Stands ",
"French ",
"Mauritius ",
"Reunion ",
"Game Meat ",
"Gastropubs ",
"Georgian ",
"German ",
"Gluten-Free ",
"Greek ",
"Guamanian ",
"Halal ",
"Hawaiian ",
"Himalayan ",
"Honduran ",
"Hong Kong Style Cafe ",
"Hot Dogs ",
"Hot Pot ",
"Hungarian ",
"Iberian ",
"Indian ",
"Indonesian ",
"Irish ",
"Italian ",
"Calabrian ",
"Sardinian ",
"Sicilian ",
"Tuscan ",
"Japanese ",
"Conveyor Belt Sushi ",
"Izakaya ",
"Japanese Curry ",
"Ramen ",
"Teppanyaki ",
"Kebab ",
"Korean ",
"Kosher ",
"Laotian ",
"Latin American ",
"Colombian ",
"Salvadoran ",
"Venezuelan ",
"Live/Raw Food ",
"Malaysian ",
"Mediterranean ",
"Falafel ",
"Mexican ",
"Tacos ",
"Middle Eastern ",
"Egyptian ",
"Lebanese ",
"European (new) ",
"Mongolian ",
"Moroccan ",
"New Mexican Cuisine ",
"Nicaraguan ",
"Noodles ",
"Pakistani ",
"Pan Asian ",
"Persian/Iranian ",
"Peruvian ",
"Pizza ",
"Polish ",
"Polynesian ",
"Pop-Up Restaurants ",
"Portuguese ",
"Poutineries ",
"Russian ",
"Salad ",
"Sandwiches ",
"Scandinavian ",
"Scottish ",
"Seafood ",
"Singaporean ",
"Slovakian ",
"Somali ",
"Soul Food ",
"Soup ",
"Southern ",
"Spanish ",
"Sri Lankan ",
"Steakhouses ",
"Supper Clubs ",
"Sushi Bars ",
"Syrian ",
"Taiwanese ",
"Tapas Bars ",
"Tapas/Small Plates ",
"Tex-Mex ",
"Thai ",
"Turkish ",
"Ukrainian ",
"Uzbek ",
"Vegan ",
"Vegetarian ",
"Vietnamese ",
"Waffles ",
"Wraps "]


class AddInterestPage(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENV.get_template('templates/InterestPage.html')
        data = {
            'Interests': Interest.query(ancestor=root_parent()).fetch(),
            'Possible_Interests': possible_interests
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


    def post(self):
        for i in range(len(possible_interests)):
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
            'data': get_restaurant_info("84.3","78.333")
        }
        print data
        self.response.write(index_template.render(data))







# class MapsPage(webapp2.RequestHandler):
#     API_KEY = "AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
#     def get(self):
#
#         user = users.get_current_user()
#         template = JINJA_ENV.get_template('templates/main.html')
#         data = {
#             'user': user,
#             'login_url': users.create_login_url(self.request.uri),
#             'logout_url': users.create_logout_url(self.request.uri),
#             "restaurants": restaurants_out,
#             "api_key": googleapikey.GOOGLE_API_KEY
#         }
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render(data))

class getCurrentLocation(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        latitude = self.request.get('lat')
        longitude = self.request.get('long')
        currentLocation = [latitude, longitude]
        content = JINJA_ENV.get_template('templates/content.html')
        food_types = get_interests_list()
        print food_types
        # returns restaurants that match user preferences
        restaurants_out = filterRestaurants(food_types,latitude,longitude)
        # adds distance and duration attributes and returns restaurants_out
        restaurants_out = getDistances(restaurants_out, currentLocation)
        sortbyDuration(restaurants_out)
        user = users.get_current_user()
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
            "restaurants": restaurants_out,
            "api_key": googleapikey.GOOGLE_API_KEY
        }
        self.response.write(content.render(data))



def filterRestaurants(user_food_types,lat,long):
    restaurants = get_restaurant_info(lat,long)
    restaurants_out = []
    for num in range(len(restaurants['businesses'])):
        categories = restaurants['businesses'][num]['categories']
        include = False
        for cat_num in range(len(categories)):
            for type in user_food_types:
                type = type[0:-1]
                if type == categories[cat_num]['title']:
                    print "INCLUDED: " + type
                    include = True
        if include == True:
            restaurants_out.append(restaurants["businesses"][num])
            print restaurants["businesses"][num]['name']

    return restaurants_out

def getDistances(restaurantsList, currentLocation):
    for restaurant in restaurantsList:
        distMatrix = get_dist_matrix(currentLocation,restaurant)
        restaurant["distance"] = distMatrix['rows'][0]['elements'][0]['distance']['text']
        restaurant["duration"] = distMatrix['rows'][0]['elements'][0]['duration']['text']
        print restaurant['name']
        print restaurant['distance']
        print restaurant['duration']
    return restaurantsList

# def get_current_location():
#     headers = {'Content-Type': 'application/json'}
#     result = urlfetch.fetch(
#              url="https://www.googleapis.com/geolocation/v1/geolocate?key=" + googleapikey.GOOGLE_API_KEY,
#              method=urlfetch.POST,
#              headers=headers)
#     return result.content

def get_dist_matrix(curLoc, rest):
    current_latitude = curLoc[0]
    current_longitude = curLoc[1]
    dest_lat = rest['coordinates']['latitude']
    dest_long = rest['coordinates']['longitude']
    distMatrixURL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(current_latitude) + "," + str(current_longitude) + "&destinations=" + str(dest_lat) + "," + str(dest_long) + "&key=" + googleapikey.GOOGLE_API_KEY
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
        restaurant['duration_int'] = duration_int
        print restaurant['name'] + ' , ' + str(restaurant['duration_int'])
    for num in range(len(restaurantsList)-1):
        j = num + 1
        while j < len(restaurantsList):
            if restaurantsList[num]['duration_int'] > restaurantsList[j]['duration_int']:
                temp = restaurantsList[num]
                restaurantsList[num] = restaurantsList[j]
                restaurantsList[j] = temp

            else:
                j+=1





# name = result['businesses'][num]['name']
# categories = result['businesses'][num]['categories'][cat_num]['title']
# latitude = result['businesses'][num]['coordinates']['latitude']
# longitude = result['businesses'][num]['coordinates']['longitude']


#this is the page where user favs are all on one page
class FavoritesPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/favorites.html')
        self.response.headers['Content-Type'] = 'text/html'
        food_types=get_interests_list()
        restaurant_favs = get_restaurant_list()
        data={
        "food_types":food_types,
        "restaurant": restaurant_favs

        }

        self.response.write(template.render(data))

class AddFavorite(webapp2.RequestHandler):
    def post(self):
        self.response.write(self.request.get("restaurantname"))
        new_interest = RestaurantInterest(parent = root_parent())
        new_interest.rest_int = self.request.get("restaurantname")

        new_interest.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest',AddInterestPage),
    ('/searchResults', searchResults),
    # ('/maps', MapsPage),
    ('/DeleteInterests', DeleteInterests),
    ('/favorites', FavoritesPage),
    ('/location', getCurrentLocation),
    ('/AddFavorite', AddFavorite)
], debug=True)
