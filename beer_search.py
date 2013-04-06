from brewerydb import *
from bs4 import BeautifulSoup

def parse_search(beer):


if __name__ == '__main__':
    BreweryDb.configure("013c7157366ad35b8e585209c7089802", "http://api.brewerydb.com/v2")
    while True:
        beer = raw_input("Enter the name of the beer you want to search: ")
        beer_info = BreweryDb.beers({"name" : beer})
        print beer_info
        while len(beer_info) < 3:
            beer = raw_input("We couldn't find this beer. Please try again: ")
            beer_info = BreweryDb.beers({"name" : beer})
        while beer_info['totalResults'] != 1:
            beer = raw_input("Did you mean any of the following: %s") \
            (beer_info['style']['category']['name'])
            beer_info = BreweryDb.beers({"name" : beer})
        label = beer_info['data'][0]['labels']['medium']
        beer_id = beer_info['data'][0]['id']
