"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""

from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlretrieve
import os
import sys

months = ['january','february','march','april','may','june','july','august','september','november','december']
herbs = ['marijuana','pot']
years = ['2008','2009','2010','2011','2012','2013','2014']

def main(url, out_folder="~/jpg_scrape/test"):
    """Downloads all the images at 'url' to /test/"""
    try:
       soup = bs(urlopen(url))
       parsed = list(urlparse.urlparse(url))

       for image in soup.findAll("img"):
           filename = image["src"].split("/")[-1]
           parsed[2] = image["src"]
           outpath = os.path.join(out_folder, month + herb + year + ".jpg")
           if "thmq" in image["src"].lower():
               print "Image: %(src)s" % image
               if image["src"].lower().startswith("http") :
                   urlretrieve(image["src"], month + herb + year + ".jpg")
               else:
                   urlretrieve(urlparse.urlunparse(parsed), month + herb + year + ".jpg")

    except HTTPError, err:
       if err.code == 404:
           print url + " not found!"
       elif err.code == 403:
           print "Access denied!"
       else:
           print "Something happened! Error code", err.code
    except URLError, err:
       print "Some other error happened:", err.reason

def _usage():
    print "usage: python dumpimages.py http://example.com [outpath]"

if __name__ == "__main__":
    out_folder = '~/jpg_scrape/test/'
    for month in months:
        for herb in herbs:
            for year in years:
                url = "http://www.hightimes.com/read/" + herb + "-prices-" + month + "-" + year + "-thmq"
                if not url.lower().startswith("http"):
                    out_folder = sys.argv[-1]
                    url = sys.argv[-2]
                    if not url.lower().startswith("http"):
                        _usage()
                        sys.exit(-1)
                main(url, out_folder)

