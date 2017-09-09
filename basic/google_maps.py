#from googlemaps import GoogleMaps
#gmaps = GoogleMaps() # no api key
#address = 'Constitution Ave NW & 10th St NW, Washington, DC'
#lat, lng = gmaps.address_to_latlng(address)
#print lat, lng


import urllib, urllib2, simplejson as json
address = 'Constitution Ave NW & 10th St NW, Washington, DC'
params = {
        'q': address,
        'output': 'json',
        'oe': 'utf8'
        }
params = urllib.urlencode(params)
url = 'http://maps.googleapis.com/maps/api/geocode/output?' + params
rawreply = urllib2.urlopen(url).read()
reply = json.loads(rawreply)
print reply
