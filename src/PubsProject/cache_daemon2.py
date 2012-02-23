
import urllib2
import datetime

def call_url(url):
    response = urllib2.urlopen(url)
    return response != None

if __name__ == "__main__":
    cache_url = "http://mingle.pl/refresh_cache"
    print "Called on: %s Success: %s" % (str(datetime.date.today()),
                                             call_url(cache_url))
