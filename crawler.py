from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import random
from news.models import News

HEADERS = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]


def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

class Crawler:
    base_url = ""
    
    def __init__(self):
        self.search_addr = "/search"

    def search(self, params, sub_url=None):
        if url is None:
            url = self.base_url+self.search_addr
        response = requests.get(url, params=params, headers={'User-Agent':random.choice(HEADERS)})
        return BeautifulSoup(response.text, 'html.parser')

https://www.cnn.com/interactive/2020/health/coronavirus-us-maps-and-cases/

class CNNCrawler(Crawler):
    base_url = "https://www.cnn.com"
    default_sub_url = "/interactive/2020/health/coronavirus-us-maps-and-cases/"

    def __init__(self):
        self.

    def search(self, params):
        soup = super().search(params)
        print(soup.prettify())
        fw = open("test.html","w")
        fw.write(soup.prettify())
        fw.close() 

        child_divs = soup.find_all('h3', recursive=True)
        print(child_divs)
        news = []
        for c_div in child_divs:
            title = c_div.find(class_="cnn-search__result-headline")   
            #print(title)         
            if title is None:
                continue
            url = title.find('a', href=True)
            title = url.text

            defaults = {}
            defaults["title"] = title.text
            defaults["category"] = None
            img = c_div.find('img')
            if img:
                defaults["image_url"] = img.get('src')
            news.append({"url":self.base_url+url['href'], 
                         "defaults":defaults})
        
        return news

if __name__ == '__main__':
