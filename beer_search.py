from brewerydb import *
from bs4 import BeautifulSoup
import urllib2
import webbrowser
from unidecode import unidecode

def get_page(beer):
    '''Str -> BeautifulSoup
    Return the resulting page from searching beer input on breweryDB.
    '''
    page = urllib2.urlopen("http://www.brewerydb.com/search?q=%s&type=beer" % (beer))
    soup = BeautifulSoup(page)
    return soup

def parse_search(soup):
    '''BeautifulSoup -> Int
    Return the number of relevant results found on page.
    '''

    results = soup.find('h3')
    found = [int(s) for s in results.string.split() if s.isdigit()]
    return found[0]

def page_and_search(beer):
    '''Str -> Int
    Return the number of results from searching beer input on breweryDB.
    '''
    page = get_page(beer)
    return parse_search(page)

def name_beers(beer):
    '''Str -> List
    Return a list with the beers found on breweryDB.
    '''
    soup = get_page(beer)
    results = []
    html_beers = soup.select('a[href^="/beer"]')
    for item in html_beers:
        if item.string:
            results.append(item.string)
    return results

def test_valid_input(beer):
    '''Str -> Str
    Test if the beer input exists in the database.
    '''

    while True:
        try:
            value = page_and_search(beer)
        except IndexError:
            beer = raw_input("We couldn't find this beer. Please try again: ").strip()
        else:
            return beer

def get_information(list_of_beers):
    '''List -> List of tuples
    Get the beer information.
    '''
    information = []
    for item in list_of_beers:
        beer = unidecode(item)
        beer_info = BreweryDb.beers({"name" : beer})
        try:
            beer_info['data'][0]['labels']['medium']
        except KeyError:
            label = "http://i.imgur.com/MKOxq58s.png"
        else:
            label = beer_info['data'][0]['labels']['medium']
        beer_id = beer_info['data'][0]['id']
        information.append((beer, beer_id, label))
    return information

def from_id(id):
    '''Str -> Tuple
    Get beer name and image from an ID.
    '''
    beer = BreweryDb.beer(id)
    try:
        beer['data']['labels']['medium']
    except KeyError:
        label = "http://i.imgur.com/MKOxq58s.png"
    else:
        label = beer['data']['labels']['medium']
    beer_name = beer['data']['name']
    return (beer_name, label)

if __name__ == '__main__':
    BreweryDb.configure("013c7157366ad35b8e585209c7089802", "http://api.brewerydb.com/v2")
    while True:
        beer = raw_input("Enter the name of the beer you want to search: ").strip()
        beer = test_valid_input(beer)
        value = page_and_search(beer)
        beer_info = BreweryDb.beers({"name" : beer})
        while len(beer_info) < 3:
            if value != 1:
                results = name_beers(beer)
                print "Did you mean any of the following:"
                for item in results:
                    print item
                beer = raw_input("Pick one: ").strip()
                test_valid_input(beer)
                beer_info = BreweryDb.beers({"name" : beer})
                value = page_and_search(beer)
