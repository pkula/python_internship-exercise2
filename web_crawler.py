import urllib
from bs4 import BeautifulSoup
import lxml
import sys


def find_core_URL(URL):
    """this function find a domain

    :Example:
    >>> find_core_URL("https://mail.google.com/mail/u/0/?tab=wm#inbox")
    https://mail.google.com
    """
    core_URL = ""
    o = 0
    for i in range(len(URL)):
        if URL[i] == "/":
            o = o + 1
        if o == 3:
            core_URL = URL[0:i]
            break
        if i == len(URL)-1:
            core_URL = URL
    return core_URL


def get_whole_link(URL, link):
    """this function return a whole link if it is incomplete

    :param1 URL: this is a core domain
    :type URL: string
    :param2 link: this is a incomplete link
    :type link: string

    :Example:
    >>>get_whole_link(http//:google.pl,"/side/rrr.html")
    http://google.pl/side/rrr.html

    """
    core_URL = find_core_URL(URL)
    if link[0:7] == "http://" or link[0:8] == "https://":
        return link
    elif link[0] == "/" and core_URL != URL:
        for i in range(len(URL)-1,0,-1):
            if URL[i] == "/" and URL != core_URL:
                return URL[:i]+link
    elif link[0] == "/" and core_URL == URL:
        return URL + link
    elif link[0:3] == "../":
        w = 0
        for i in range(len(URL)-1,0,-1):
            if URL[i] == "/":
                w=w+1
            if w == 2:
                return URL[:i] + link[2:]
    else:
        return link    


def add_protocol(adress):
    """this function add protocol if adress don't have it

    :Example:
    >>>add_protocol(google.pl)
    http://:google.pl
    """
    if adress[0:3] == "www":
        return "http://" + adress
    elif adress[0:7] == "http://" or adress[0:8] == "https://":
        return adress
    else:
        return "http://www."+ adress


def map_one_site(URL):
    """this function create dictionary with all links in this domain

    :param URL: this is site which we mapping
    :param: string

    :Example:
    >>>map_one_site("http://0.0.0.0:8000")
    http://0.0.0.0:8000
    {'title': 'Index', 'links': {'http://0.0.0.0:8000/example.html', 'http:0.0.0.0:8000site.html'}}
    """
    try:
        URL = add_protocol(URL)
        core_URL = find_core_URL(URL)
        soup = BeautifulSoup(urllib.request.urlopen(URL).read(),"lxml")
        title = (str(soup.find("title"))[7:-8])
        links = []
        for link in soup.find_all("a"):
            link = link.get("href")
            if link == "#":
                continue
            link = get_whole_link(URL, link)       
            if link[0:len(core_URL)] != core_URL:
                continue
            links.append(link) 
        dictionary = {
        "title":title,
        "links":set(links)
        }
        return [URL, dictionary]
    except:
        print("critical error", file=sys.stderr)


def site_map(URL):
    """this function site_map(url) that takes a site URL as an argument and creates a mapping
    of that domain as a Python dictionary.
    The mapping contain all the accessible pages within that domain. Entry
    consist of:
        * key: URL
        * value: dictionary with:
        ** site title (HTML `<title>` tag)
        ** links - set of all target URLs within the domain on the page but without anchor links
    
    :param URL: this is site which we would like to create map
    :param: string

    :Example: 
    >>>site_map("http://0.0.0.0:8000")

    http://0.0.0.0:8000
    {'title': 'Index', 'links': {'http://0.0.0.0:8000/example.html', 'http:0.0.0.0:8000site.html'}}


    http://0.0.0.0:8000/example.html
    {'title': 'No links here', 'links': set()}


    http://0.0.0.0:8000/site.html
    {'title': 'The Site', 'links': {'http://0.0.0.0:8000/site/subsite.html'}}


    http://0.0.0.0:8000/site/subsite.html
    {'title': 'Looping', 'links': {'http://0.0.0.0:8000/site/other_site.html', 'http0.0.0.0:8000'}}


    http://0.0.0.0:8000/site/other_site.html
    {'title': 'Looped', 'links': {'http://0.0.0.0:8000/site/subsite.html'}}
    """
    dictionary = {}
    num_record_in_dict = 0
    t = map_one_site(URL)
    dictionary[t[0]] = t[1]
    while num_record_in_dict != len(dictionary):
        num_record_in_dict = len(dictionary)
        for link in t[1]["links"]:
            if link not in dictionary:
                t = map_one_site(link)
                dictionary[t[0]] = t[1]
    return dictionary
