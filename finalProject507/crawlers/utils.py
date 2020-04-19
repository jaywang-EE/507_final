import requests
import json
from bs4 import BeautifulSoup
from time import strptime
from datetime import datetime, timedelta
from .secrets import *
from djangoherokuapp import settings

CACHE_FILENAME = "cache_covid.json"

def get_newsAPI(query="virus", date=None):
    print("calling get_newsAPI")
    if not date:
        date = datetime.now() - timedelta(days=1)
    url = "http://newsapi.org/v2/everything?q=virus%20michigan&from=2020-04-04&sortBy=publishedAt&apiKey=9fc059554b904b57b0870a1c8921fdab"
    params = {"q":query, "from":date.strftime("%Y-%m-%d"), "sortBy":"popularity", "apiKey":NEWS_API_KEY}
    return get_soup(url, params, True)

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
    print("saving")
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def get_soup(url, params=None, is_json=False):
    if not settings.ON_HEROKU:
        cache = open_cache()
        if "html" not in cache:
            cache["html"] = {}
        if url not in cache["html"]:
            response = requests.get(url, params=params)
            if is_json:
                cache["html"][url] = response.json()
            else:
                cache["html"][url] = BeautifulSoup(response.text, 'html.parser')
            save_cache(cache)

        return cache["html"][url]
    else:
        response = requests.get(url, params=params)
        if is_json:
            return response.json()
        else:
            return BeautifulSoup(response.text, 'html.parser')

def get_soup_ajax(browser, url):
    browser.get(url)
    browser.implicitly_wait(3)
    return BeautifulSoup(browser.page_source, 'html.parser')

def comma_str2int(s):
    return int(s.replace(',', ''))

def download_github(url):
    response = requests.get(url)
    return response.text.split("\n")

def monthToInt(m):
    return strptime(m,'%b').tm_mon

