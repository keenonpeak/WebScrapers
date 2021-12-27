import praw
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(client_id='bx2hqlSd22o6RgSCnfqHBw',
                     client_secret='qqVB9BQbAAlX65OTFKJUuj8GO-Epag',
                     user_agent='Web scrapping')

data = []
for posts in reddit.subreddit("all").search("Barco clickshare", sort="comments", limit=None):
    try:
        submission = reddit.submission(url=str(posts.url))
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            unix_time = comment.created_utc
            FilterComma = comment.body.replace(",", ";")
            data.append([submission.title, FilterComma.encode("utf-8"), datetime.fromtimestamp(unix_time).strftime("%Y-%m-%dT%H:%M:%SZ")])
            print(str(datetime.fromtimestamp(unix_time)))
    except:
        pass
data = pd.DataFrame(data, columns=[ 'Title', 'Comments', 'EventTime'])
data.to_csv('DataFromReddit.csv', index=False)
# sort the csv via timestamp
csvData = pd.read_csv("DataFromReddit.csv")
csvData.sort_values(["EventTime"],
                    axis=0,
                    ascending=[False],
                    inplace=True)
csvData.to_csv('DataFromReddit.csv', index=False)
