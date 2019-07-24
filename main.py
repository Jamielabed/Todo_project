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


class Interest(ndb.Model):
    interests = ndb.StringProperty()

def get_restaurant_info(lat,long):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+yelpapikey.YELP_API_KEY}

    result_unformatted = urlfetch.fetch(
        #payload = form_data,
        method=urlfetch.GET,
        url = "https://api.yelp.com/v3/businesses/search?latitude="+str(lat)+"&longitude="+str(long),
        headers=headers).content
    result = json.loads(result_unformatted)
    return result
def get_interests_list():
    existing_interests = Interest.query(ancestor = root_parent()).fetch()
    interests_list = []
    for interest in existing_interests:
        interests_list.append(interest.interests)
    return interests_list


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('templates/main.html')

        data = {
                 'user': user,
                 'login_url': users.create_login_url(self.request.uri),
                 'logout_url': users.create_logout_url(self.request.uri),
                 "api_key": googleapikey.GOOGLE_API_KEY
                }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

possible_interests =["Afghan", "African", "Senegalese", "Afghan (afghani)",
"African (african)",
"Senegalese (senegalese)",
"South African (southafrican)",
"American (New) (newamerican)",
"American (Traditional) (tradamerican)",
"Arabian (arabian)",
"Argentine (argentine)",
"Armenian (armenian)",
"Asian Fusion (asianfusion)",
"Australian (australian)",
"Austrian (austrian)",
"Bangladeshi (bangladeshi)",
"Barbeque (bbq)",
"Basque (basque)",
"Belgian (belgian)",
"Brasseries (brasseries)",
"Brazilian (brazilian)",
"Breakfast & Brunch (breakfast_brunch)",
"Pancakes (pancakes)",
"British (british)",
"Buffets (buffets)",
"Bulgarian (bulgarian)",
"Burgers (burgers)",
"Burmese (burmese)",
"Cafes (cafes)",
"Themed Cafes (themedcafes)",
"Cafeteria (cafeteria)",
"Cajun/Creole (cajun)",
"Cambodian (cambodian)",
"Caribbean (caribbean)",
"Dominican (dominican)",
"Haitian (haitian)",
"Puerto Rican (puertorican)",
"Trinidadian (trinidadian)",
"Catalan (catalan)",
"Cheesesteaks (cheesesteaks)",
"Chicken Shop (chickenshop)",
"Chicken Wings (chicken_wings)",
"Chinese (chinese)",
"Cantonese (cantonese)",
"Dim Sum (dimsum)",
"Hainan (hainan)",
"Shanghainese (shanghainese)",
"Szechuan (szechuan)",
"Comfort Food (comfortfood)",
"Creperies (creperies)",
"Cuban (cuban)",
"Czech (czech)",
"Delis (delis)",
"Diners (diners)",
"Dinner Theater (dinnertheater)",
"Eritrean (eritrean)",
"Ethiopian (ethiopian)",
"Fast Food (hotdogs)",
"Filipino (filipino)",
"Fish & Chips (fishnchips)",
"Fondue (fondue)",
"Food Court (food_court)",
"Food Stands (foodstands)",
"French (french)",
"Mauritius (mauritius)",
"Reunion (reunion)",
"Game Meat (gamemeat)",
"Gastropubs (gastropubs)",
"Georgian (georgian)",
"German (german)",
"Gluten-Free (gluten_free)",
"Greek (greek)",
"Guamanian (guamanian)",
"Halal (halal)",
"Hawaiian (hawaiian)",
"Himalayan/Nepalese (himalayan)",
"Honduran (honduran)",
"Hong Kong Style Cafe (hkcafe)",
"Hot Dogs (hotdog)",
"Hot Pot (hotpot)",
"Hungarian (hungarian)",
"Iberian (iberian)",
"Indian (indpak)",
"Indonesian (indonesian)",
"Irish (irish)",
"Italian (italian)",
"Calabrian (calabrian)",
"Sardinian (sardinian)",
"Sicilian (sicilian)",
"Tuscan (tuscan)",
"Japanese (japanese)",
"Conveyor Belt Sushi (conveyorsushi)",
"Izakaya (izakaya)",
"Japanese Curry (japacurry)",
"Ramen (ramen)",
"Teppanyaki (teppanyaki)",
"Kebab (kebab)",
"Korean (korean)",
"Kosher (kosher)",
"Laotian (laotian)",
"Latin American (latin)",
"Colombian (colombian)",
"Salvadoran (salvadoran)",
"Venezuelan (venezuelan)",
"Live/Raw Food (raw_food)",
"Malaysian (malaysian)",
"Mediterranean (mediterranean)",
"Falafel (falafel)",
"Mexican (mexican)",
"Tacos (tacos)",
"Middle Eastern (mideastern)",
"Egyptian (egyptian)",
"Lebanese (lebanese)",
"Modern European (modern_european)",
"Mongolian (mongolian)",
"Moroccan (moroccan)",
"New Mexican Cuisine (newmexican)",
"Nicaraguan (nicaraguan)",
"Noodles (noodles)",
"Pakistani (pakistani)",
"Pan Asian (panasian)",
"Persian/Iranian (persian)",
"Peruvian (peruvian)",
"Pizza (pizza)",
"Polish (polish)",
"Polynesian (polynesian)",
"Pop-Up Restaurants (popuprestaurants)",
"Portuguese (portuguese)",
"Poutineries (poutineries)",
"Russian (russian)",
"Salad (salad)",
"Sandwiches (sandwiches)",
"Scandinavian (scandinavian)",
"Scottish (scottish)",
"Seafood (seafood)",
"Singaporean (singaporean)",
"Slovakian (slovakian)",
"Somali (somali)",
"Soul Food (soulfood)",
"Soup (soup)",
"Southern (southern)",
"Spanish (spanish)",
"Sri Lankan (srilankan)",
"Steakhouses (steak)",
"Supper Clubs (supperclubs)",
"Sushi Bars (sushi)",
"Syrian (syrian)",
"Taiwanese (taiwanese)",
"Tapas Bars (tapas)",
"Tapas/Small Plates (tapasmallplates)",
"Tex-Mex (tex-mex)",
"Thai (thai)",
"Turkish (turkish)",
"Ukrainian (ukrainian)",
"Uzbek (uzbek)",
"Vegan (vegan)",
"Vegetarian (vegetarian)",
"Vietnamese (vietnamese)",
"Waffles (waffles)",
"Wraps (wraps)"]
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
        # REMOVE WHEN FOOD TYPES INPUT = WORKING
        food_types = ["Pizza", "Italian"]
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
                if type == categories[cat_num]['title']:
                    include = True
        if include == True:
            restaurants_out.append(restaurants["businesses"][num])
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



class FavoritesPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('templates/favorites.html')
        self.response.headers['Content-Type'] = 'text/html'
        food_types = get_interests_list()
        data = {
            "food_types": food_types
        }
        self.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/AddInterest',AddInterestPage),
    ('/searchResults', searchResults),
    # ('/maps', MapsPage),
    ('/DeleteInterests', DeleteInterests),
    ('/favorites', FavoritesPage),
    ('/location', getCurrentLocation)
], debug=True)
