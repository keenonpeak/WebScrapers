from fake_useragent import UserAgent
import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import time
import math
from tqdm.auto import tqdm
from random import choice
from requests_html import HTMLSession
from datetime import datetime 

# to ignore SSL certificate errors
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# random user-agent
ua = UserAgent()


class amazon_product_review_scraper:

    def __init__(self, amazon_site, product_asin, sleep_time=0.01, start_page=1, end_page=None):
        self.url = "https://www." + amazon_site + \
            "/dp/product-reviews/" + product_asin + "?pageNumber={}"
        self.sleep_time = sleep_time
        self.max_try = 100000
        self.proxies = self.proxy_generator()
        self.ua = ua.random
        self.proxy = choice(self.proxies)
        self.data = []
        self.start_page = start_page
        if (end_page == None):
            self.end_page = self.total_pages()
        else:
            self.end_page = min(end_page, self.total_pages())

    def total_pages(self):
        response = self.request_wrapper(self.url.format(1))
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find_all(
            "div", {"data-hook": "cr-filter-info-review-rating-count"})
        total_reviews = int(content[0].find_all("span")[0].get_text(
            "\n").strip().split(" ")[4].replace(",", ""))
        print("Total reviews (all pages): {}".format(total_reviews), flush=True)
        total_pages = math.ceil(total_reviews/10)
        return total_pages

    # function to scrape event time and review's country on every pages
    def helper(self, review, tag, parameter_key, parameter_value):
        attributes = review.find_all(tag, {parameter_key: parameter_value})
        timeList = []
        Countrylist = []
        dic = {"January":1,
        "February":2,
        "March":3,
        "April":4,
        "May":5,
        "June":6,
        "July":7,
        "August":8,
        "September":9,
        "October":10,
        "November":11,
        "December":12}
        for timeStamp in attributes:
            orgTime = timeStamp.contents[0]
            afterStrip = orgTime.strip("Reviewed in")
            afterReplace = afterStrip.replace(",", "")
            afterSplit = afterReplace.split()
            if afterSplit[-2] in dic:
                evemtTime = datetime(int(afterSplit[-1]), int(dic[afterSplit[-2]]), int(afterSplit[-3])).strftime("%Y-%m-%dT%H:%M:%SZ")
                timeList.append(evemtTime)
            else:
                evemtTime = datetime(int(afterSplit[-1]), int(dic[afterSplit[-3]]), int(afterSplit[-2])).strftime("%Y-%m-%dT%H:%M:%SZ")
                timeList.append(evemtTime)
            if afterSplit[0] == 'the':
                Countrylist.append(afterSplit[0] + " "+ afterSplit[1] + " " + afterSplit[2])
            else:
                Countrylist.append(afterSplit[0])

        # content
        contents = review.find_all("span", {"data-hook": "review-body"})
        i = 0
        for content in contents:  
            text_ = content.find_all("span")[0].get_text("\n").strip()
            self.data.append([text_, timeList[i], Countrylist[i]])
            i += 1

    def page_scraper(self, page):
        response = self.request_wrapper(self.url.format(page))
        # parsing content
        soup = BeautifulSoup(response.text, 'html.parser')
        # reviews section
        reviews = soup.findAll(
            "div", {"class": "a-section review aok-relative"})
        # parsing reviews section
        reviews = BeautifulSoup(
            '<br/>'.join([str(tag) for tag in reviews]), 'html.parser')
        # using helper to scrape reviews and timeStamp on every pages
        self.helper(reviews, "span", "data-hook", "review-date")
        self.ua = ua.random
        self.proxy = choice(self.proxies)

    # wrapper around request package to make it resilient
    def request_wrapper(self, url):
        while (True):
            # amazon blocks requests that does not come from browser, therefore need to mention user-agent
            response = requests.get(url, verify=False, headers={
                                    'User-Agent': self.ua}, proxies=self.proxy)
            # checking the response code
            if (response.status_code != 200):
                raise Exception(response.raise_for_status())
            # checking whether capcha is bypassed or not (status code is 200 in case it displays the capcha image)
            if "api-services-support@amazon.com" in response.text:
                if (self.max_try == 0):
                    raise Exception("CAPTCHA is not bypassed")
                else:
                    time.sleep(self.sleep_time)
                    self.max_try -= 1
                    self.ua = ua.random
                    self.proxy = choice(self.proxies)
                    print(self.ua)
                    print(self.proxy)
                    continue
            self.max_try = 100000
            break
        return response

    # random proxy generator
    def proxy_generator(self):
        proxies = []
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'html.parser')
        proxies_table = soup.find("table", {"class": "table table-striped table-bordered"})
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                'ip':   row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
            })

        proxies_lst = [{'http': 'http://'+proxy['ip'] +
                        ':'+proxy['port']} for proxy in proxies]
        return proxies_lst

        # MAIN FUNCTION
    def scrape(self):
        print("Total pages: {}".format(
            self.end_page - self.start_page+1), flush=True)
        print("Start page: {}; End page: {}".format(
            self.start_page, self.end_page))
        print()
        print("Started!", flush=True)
        for page in tqdm(range(self.start_page, self.end_page+1)):
            self.page_scraper(page)
            time.sleep(self.sleep_time)
        print("Completed!")
        # returning data
        return(self.data)


# Scrape ASIN from Amazon
url = 'https://www.amazon.com/s?k=barco+clickshare&ref=nb_sb_noss_1'
amazon_ver = "amazon.com"
s = HTMLSession()
r = s.get(url)
r.html.render(sleep=0.01)
items = r.html.find('div[data-asin]')
Data = []
# go through all the ASIN and scrape all reviews
for item in items:
    if item.attrs['data-asin'] != '':
        ASIN = item.attrs['data-asin']
        print(ASIN)
        review_scraper = amazon_product_review_scraper(
            amazon_ver, product_asin=ASIN)
        reviews_per_post = review_scraper.scrape()
    Data += reviews_per_post
Data = pd.DataFrame(Data, columns=['Comment', 'EventTime', 'Country'])
Data.to_csv('DataFromAmazon.csv', index=False)
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromAmazon.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromAmazon.csv', index = False)