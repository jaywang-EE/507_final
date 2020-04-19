from .utils import *
import time
from ..models import Order

# for NY
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from djangoherokuapp import settings


GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def get_news():
    return get_newsAPI()

def craw_gov():
    orders = craw_gov_michgan()
    print(len(orders))
    if orders:
        for order in orders:
            new_order = Order(title=order['title'], url=order['url'], date=order['date'], stateName="MI")
            new_order.save()

    orders = craw_gov_newjersey()
    print(len(orders))
    if orders:
        for order in orders:
            new_order = Order(title=order['title'], url=order['url'], date=date.today(), stateName="NJ")
            new_order.save()

    orders = craw_gov_newyork()
    print(len(orders))
    if orders:
        for order in orders:
            new_order = Order(title=order['title'], url=order['url'], date=order['date'], stateName="NY")
            new_order.save()

    return ["MI", "NJ", "NY"]

def craw_gov_michgan():
    url = "https://www.michigan.gov/coronavirus/0,9753,7-406-98158---,00.html"
    root_url = "https://www.michigan.gov"
    soup = get_soup(url)

    divs = soup.find("div", class_="monthlyIndex").find_all("div", class_="indexRow", recursive=False)

    news = []
    for div in divs:
        try:
            title = div.find("a", class_="bodylinks")
            d     = int(div.find("span", class_="date").text)
            m     = monthToInt(div.find("span", class_="month").text)
            y     = int(div.find("span", class_="year").text)

            date = datetime.strptime("%d-%02d-%02d"%(y, m, d), '%Y-%m-%d')

            if (Order.objects.filter(date__gte=date).exists()):
                return news

            news.append({"title": title.text, "url": root_url+title["href"], "date": date})
        except:
            print("can't parse craw_gov_michgan: "+str(div))

    return news

def craw_gov_newjersey():
    url = "https://covid19.nj.gov/faqs/announcements"
    root_url = "https://covid19.nj.gov/"

    soup = get_soup(url)

    divs = soup.find("ul", class_="FAQTeaser-list").find_all("li", recursive=False)

    news = []
    for div in divs:
        try:
            title = div.find("h3", recursive=False).text
            sub_url   = div.find("a", recursive=False)["href"][3:]
            if (Order.objects.filter(url=(root_url+sub_url)).exists()):
                return news

            news.append({"title": title, "url": root_url+sub_url, "date": None})
        except:
            print("can't parse craw_gov_michgan: "+str(div))
    return news

def craw_gov_newyork(on_heroku=False, from_days_ago=90):
    # from https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    from_date = datetime.now() - timedelta(days=from_days_ago)
    url = "https://www1.nyc.gov/office-of-the-mayor/news.page"
    root_url = "https://www1.nyc.gov/office-of-the-mayor/news"


    if settings.ON_HEROKU:
        browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome(ChromeDriverManager().install())

    print("start crawling NY...")

    browser.get(url)
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    main_div = soup.find("div", class_="inner")
    divs = main_div.find("ul", class_="list-items span12", recursive=False).find_all("li", recursive=False)
    
    next_page = soup.find("a", class_="page-link next")["href"]

    news = []
    ctr = 1
    while True:
        for div in divs:
            div_detail = div.find("div", class_="event-data-detail")
            title = div_detail.find("h4").find("a")
            date  = div_detail.find("label")
            if date:
                date = datetime.strptime(date.text,'%b %d, %Y')
                if (date < from_date) or (Order.objects.filter(date__gte=date).exists()):
                    return news
            else:
                print(div)
            news.append({"title": title.text, "url": root_url+title["href"], "date": date})

        try:
            time.sleep(0.5)
            ctr += 1
            print("next_page:", ctr)
            browser.find_element_by_xpath("//a[@class='page-link next']").click()
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            main_div = soup.find("div", class_="inner")
            divs = main_div.find("ul", class_="list-items span12", recursive=False).find_all("li", recursive=False)
        except:
            print("finish")
            break
    return news

if __name__ == '__main__':
    print(get_news())