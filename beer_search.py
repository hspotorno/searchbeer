from brewerydb import *
from bs4 import BeautifulSoup
import urllib2
import webbrowser

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

if __name__ == '__main__':
    BreweryDb.configure("013c7157366ad35b8e585209c7089802", "http://api.brewerydb.com/v2")
    while True:
        beer = raw_input("Enter the name of the beer you want to search: ")
        value = page_and_search(beer)
        beer_info = BreweryDb.beers({"name" : beer})
        while len(beer_info) < 3 and value != 1:
            if value != 1:
                results = name_beers(beer)
                beer = raw_input("Did you mean any of the following: %s " \
                    %(results))
                beer_info = BreweryDb.beers({"name" : beer})
                value = parse_search(beer)
            elif len(beer_info) < 3:
                beer = raw_input("We couldn't find this beer. Please try again: ")
                beer_info = BreweryDb.beers({"name" : beer})
                value = parse_search(beer)
        print beer_info
        if beer_info['data'][0]['labels']['medium']:
            label = beer_info['data'][0]['labels']['medium']
        beer_id = beer_info['data'][0]['id']
        webbrowser.open("http://www.brewerydb.com/beer/%s" %(beer_id))