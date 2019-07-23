from google.appengine.ext import ndb

class Restaruant(ndb.Model):
    student_num =  ndb.IntegerProperty(required=True)
    first_name =  ndb.StringProperty(required=True)
    last_name =  ndb.StringProperty(required=True)
    # house_name is the house this student belongs to so there is a
    # corresponding House entry with House.name == Student.house_name
    house_name = ndb.StringProperty(required=True)
