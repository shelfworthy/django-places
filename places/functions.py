import urllib, logging

try:
    from xml.etree import cElementTree as ET
except ImportError:
    import cElementTree as ET

from geopy import geocoders

from django.conf import settings

from .models import Place
from .exceptions import PlaceException

KML_NS = 'http://earth.google.com/kml/2.0'
KML_NS2 = 'urn:oasis:names:tc:ciq:xsdschema:xAL:2.0'

log = logging.getLogger('places.functions')

def get_place_from_name(place):
    g = geocoders.Google(settings.GOOGLE_API_KEY)
    
    try:
        place, (lat, lng) = g.geocode(place)
    except ValueError:
        return None
    
    return _get_place_object(lat, lng, place)

def get_place_from_zip(zipcode):
    g = geocoders.Google(settings.GOOGLE_API_KEY)
    
    try:
        place, (lat, lng) = g.geocode(zipcode)
    except ValueError:
        return None
    
    return _get_place_object(lat, lng, place, zipcode)

def get_place_from_cords(lat, lng):
    # TODO update this when geopy supports reverse geocoding (should be soon)
    log.debug("In get place with lat/long %s/%s" % (lat, lng))
    resp = get_place_response(lat, lng)
    tree = parse_place(resp)
    place_response = get_place_from_tree(tree)
    return _get_place_object(lat, lng, place_response)

class PlaceResponse(object):
    def __init__(self, place, state, country):
        self.place = place
        self.state = state
        self.country = country
        self.name = ""
        
        if state:
            if country:
                self.name = state + ", "
            else:
                self.name = state
        if country:
            self.name = self.name + country
        
        if place:
            self.name = place + ', ' + self.name
        
        if self.name == "":
            self.name = "Unknown Place"

def get_place_from_tree(tree):
    status = tree.find(_node('.//Status')).find(_node('code')).text
    if status != '200':
        raise PlaceException("Status code from Google was %s" % status)
    
    place = tree.find(_node('.//LocalityName', ns=KML_NS2))
    if place is not None:
        place = place.text
    state = tree.find(_node('.//AdministrativeAreaName', ns=KML_NS2))
    if state is not None:
        state = state.text
    country = tree.find(_node('.//CountryName', ns=KML_NS2))
    if country is not None:
        country = country.text
    return PlaceResponse(place, state, country)

def _node(name, ns=KML_NS):
    if './/' in name:
        # Move the path outside the namespace
        return ".//{%s}%s" % (ns, name.replace('.//', ''))
    return u"{%s}%s" % (ns, name)
        
def get_place_response(lat, lng):
    return urllib.urlopen("http://maps.google.com/maps/geo?q=%s,%s&output=xml&oe=utf-8&key=%s" % (lat,lng,settings.GOOGLE_API_KEY)).read()

def parse_place(resp):
    return ET.fromstring(resp)

def _get_place_object(lat, lng, place_response=None, zipcode=None):
    place, created = Place.objects.get_or_create(latitude=lat, longitude=lng)
    
    if created:
        if place_response:
            place.name = place_response.name
        if zipcode:
            place.zipcode = zipcode
        place.save()
    
    return place
