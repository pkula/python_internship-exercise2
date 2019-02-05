import urllib
from bs4 import BeautifulSoup
import lxml
import sys




def find_core_URL(URL):
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



def get_all_link(core_URL, URL, link):
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
    if adress[0:3] == "www":
        return "http://" + adress
    elif adress[0:7] == "http://" or adress[0:8] == "https://":
        return adress
    else:
        return "http://www."+ adress


def map_one_site(URL):
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

            link = get_all_link(core_URL, URL, link)
            
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
    dictionary = {}
    t = map_one_site(URL)
    dictionary[t[0]] = t[1]
    print(dictionary)



site_map("krkmeble.pl")
print("\n")
site_map("http://0.0.0.0:8000")
print("\n")
site_map("http://0.0.0.0:8000/site.html")
print("\n")
site_map("http://0.0.0.0:8000/example.html")
print("\n")
site_map("http://0.0.0.0:8000/site/subsite.html")
print("\n")
site_map("http://0.0.0.0:8000/site/other_site.html")
print("\n")
