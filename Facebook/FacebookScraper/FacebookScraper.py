from facebook_scraper import get_posts
import pandas as pd

data = []
for post in get_posts('ClickShareBarco', pages = 4, extra_info = True, options = {"comments": True, "posts_per_page": 250}):
    try:
        if "clickshare" or "Clickshare" or "ClickShare" in post['text'][::]:
            commaFilter = post['text'][::].replace(",", ";")
            data.append([commaFilter.encode("utf-8"), post['time'].strftime("%Y-%m-%dT%H:%M:%SZ"), post['username'][::], post['likes'], post['comments'], post['shares']])
            print("first:" + str(post['time']))
        else:
            print("first excluded")
    except:
        print("first x")
for post in get_posts('barco.bangladesh', pages = 4, extra_info = True, options = {"comments": True, "posts_per_page": 250}):
    try:
        if "clickshare" or "Clickshare" or "ClickShare" in post['text'][::]:
            commaFilter = post['text'][::].replace(",", ";")
            data.append([commaFilter.encode("utf-8"), post['time'].strftime("%Y-%m-%dT%H:%M:%SZ"), post['username'][::], post['likes'], post['comments'], post['shares']])
            print("second:" + str(post['time']))
        else:
            print("second excluded")
    except:
        print("second x")
for post in get_posts('techrepublicltd', pages = 4, extra_info = True, options = {"comments": True, "posts_per_page": 250}):
    try:
        if "clickshare" or "Clickshare" or "ClickShare" in post['text'][::]:
            commaFilter = post['text'][::].replace(",", ";")
            data.append([commaFilter.encode("utf-8"), post['time'].strftime("%Y-%m-%dT%H:%M:%SZ"), post['username'][::], post['likes'], post['comments'], post['shares']])
            print("third:" + str(post['time'])) 
        else:
            print("third excluded")
    except:
        print("thrid x")
for post in get_posts('ceecotechnologies', pages = 4, extra_info = True, options = {"comments": True, "posts_per_page": 250}):
    try:
        if "clickshare" or "Clickshare" or "ClickShare" in post['text'][::]:
            commaFilter = post['text'][::].replace(",", ";")
            data.append([commaFilter.encode("utf-8"), post['time'].strftime("%Y-%m-%dT%H:%M:%SZ"), post['username'][::], post['likes'], post['comments'], post['shares']])
            print("fourth:" + str(post['time']))
        else:
            print("fourth excluded")
    except:
        print("fourth x")
data = pd.DataFrame(data, columns=['Content', 'EventTime', 'Username', 'Likes', 'Comments', 'Shares'])
data.to_csv('DataFromFacebook.csv', index=False)
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromFacebook.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromFacebook.csv', index = False)