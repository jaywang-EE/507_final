from .utils import *
from ..models import County, CountyCase
from django.db.models import Max
from djangoherokuapp import settings

COUNTY_DATA_URL = "https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv"
STATE_DATA_URL  = "https://github.com/nytimes/covid-19-data/raw/master/us-states.csv"


def update_data_county(data, cache):
    print("Start update county...")
    data = data[1:]
    data = data[::-1]

    if cache is None:
        cache = []
    
    max_date = CountyCase.objects.all().aggregate(Max('date'))["date__max"]

    cache = County.objects.distinct("stateName").values("stateName")
    cache = [row["stateName"] for row in cache]

    if CountyCase.objects.all().count() >= len(data):
        return cache

    current_date = None
    for i, row in enumerate(data):
        if i%100 == 0:
            print("%d/%d: %s | %d"%((i+1), len(data), row, CountyCase.objects.all().count()))
        
        if 1:
            date, county, state, fips, cases, deaths = row.split(',') 
            
            date = datetime.strptime(date, '%Y-%m-%d')

            if (not settings.ON_HEROKU) and max_date and date.date() < max_date:
                break

            fips = int(fips) if fips else -1
            cases = int(cases)
            deaths = int(deaths)

            new_county, created = County.objects.get_or_create(stateName=state, countyName=county,
                                                               defaults={'fip': fips})

            CountyCase.objects.get_or_create(county=new_county, date=date, defaults={"deaths":deaths, "cases":cases})
        try:
            pass
        except:
            print("ERROR: "+row)

    return cache

def get_county_data(cache):
    data = download_github(COUNTY_DATA_URL)
    return update_data_county(data, cache)

def get_state_data():
    data = download_github(STATE_DATA_URL)
    return data

"""
MAIN_URL = "https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html#map"
def get_county():
    soup = get_soup(MAIN_URL)
    states = soup.find("div", class_="g-footer-asset").find("ul", class_="columns svelte-mmjzxm").find_all("li", recursive=False)
    for state in states:
        url = state.find("a")["href"]
        print(state.text, url)
        craw_state(url)

def craw_state(state_url):
    soup = get_soup(state_url)
    total = soup.find("div", id="cases-top-presentation").find("div", class_="counts svelte-1aesbb8").find_all("div", recursive=False)
    total_comfirmed = comma_str2int(total[0].find_all("div", recursive=False)[1].text)
    total_death     = comma_str2int(total[1].find_all("div", recursive=False)[1].text)

    table = soup.find("div", id="county").find("table").find("tbody")
    print(table)
"""
