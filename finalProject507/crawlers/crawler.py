from datetime import datetime
from . import crawler_cases
from . import crawler_news
from . import utils
from djangoherokuapp import settings

def craw_covid():
    cache = utils.open_cache()
    print(cache)
    if settings.ON_HEROKU:
        if not cache:
            print("empty cache!")
            cache = {
                "orders": crawler_news.craw_gov(),
                "county": crawler_cases.get_county_data(cache.get("county")),
                "last_update": datetime.now().strftime("%Y-%m-%d"),
            }
            utils.save_cache(cache)

    elif not cache or ("last_update" not in cache or cache["last_update"] != datetime.now().strftime("%Y-%m-%d")):
        cache = {
            "county": crawler_cases.get_county_data(cache.get("county")),
            #"news": crawler_news.get_news(),
            "orders": crawler_news.craw_gov(),
            "last_update": datetime.now().strftime("%Y-%m-%d"),
        }
        utils.save_cache(cache)
    return cache

def craw_covid_cron():
    cache = utils.open_cache()
    print("start cron...")
    cache = {
        "orders": crawler_news.craw_gov(),
        "county": crawler_cases.get_county_data(cache.get("county")),
        #"news": crawler_news.get_news(),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
    }
    print(cache)
    utils.save_cache(cache)

if __name__ == '__main__':
    craw_covid()