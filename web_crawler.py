import urllib
from bs4 import BeautifulSoup
import lxml


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


def site_map(URL):
    core_URL = find_core_URL(URL)
    soup = BeautifulSoup(urllib.request.urlopen(URL).read(),"lxml")
    title = (str(soup.find("title"))[7:-8])
    links = []
    for link in soup.find_all("a"):
        link = link.get("href")
        if link == "#":
            continue
        if link[0]=="/":
            link = core_URL + link
        if link[0:len(core_URL)] != core_URL:
            continue
        links.append(link)
        
    dictionary = {URL: {
    "title":title,
    "links":set(links)}
    }
    
    print(dictionary)


site_map("http://0.0.0.0:8000")
print("\n\n")
site_map("http://0.0.0.0:8000/site.html")
print("\n\n")
site_map("http://0.0.0.0:8000/example.html")
print("\n\n")
site_map("http://0.0.0.0:8000/site/subsite.html")
print("\n\n")
site_map("http://0.0.0.0:8000/site/other_site.html")

site_map("http://www.krkmeble.pl/")

