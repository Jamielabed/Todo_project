from google.appengine.ext import ndb

class Restaurant(ndb.Model):
    rating =  ndb.IntegerProperty(required=True)
    restaurant_name =  ndb.StringProperty(required=True)
    address =  ndb.StringProperty(required=True)
