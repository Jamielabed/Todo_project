# https://maps.googleapis.com/maps/api/distancematrix/json?origins=Seattle&destinations=San+Francisco&key=YOUR_API_KEY
API_KEY = AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE
def post(self):
    currentLocation = https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE

def get(self):
    chicago = {
        name = "Chicago"
    }
    seattle = {
        name = "Seattle"
    }
    restaurantsList = [chicago, seattle]
    for restaurant in restaurantsList:
        # separate words in destination should be separated w + (San+Francisco) --> not implemented, see if affects output
        # ^^ put into lat/long so shouldn't be an issue
        latitude = currentLocation.location.lat
        longitude = currentLocation.location.lng
        distMatrix = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + latitude + "," + longitude + "&destinations=" + restaurant.name + "&key=AIzaSyAfFZHWxBjkkd8vi12mY4d3IOaDHdBkuWE"
        restaurant.distance = distMatrix.rows[0].elements[0].distance.text
        restaurant.duration = distMatrix.rows[0].elements[0].duration.text
