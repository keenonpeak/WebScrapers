import twint
import pandas as pd
from datetime import datetime 

c = twint.Config()
c.Custom["tweet"] = ["tweet", "date", "username", "hashtags", "likes_count", "replies_count", "retweets_count"]
c.Search = "clickshare"
c.Store_csv = True
c.Output = "DataFromTwitter.csv"
twint.run.Search(c)
# change the time stamp to ISO format
df = pd.read_csv('DataFromTwitter.csv', skiprows=0)
orgDate = df.date
timeList = []
for date in orgDate:
    afterSplit = date.split("-")
    eventTime = datetime(int(afterSplit[-3]), int(afterSplit[-2]), int(afterSplit[-1])).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(eventTime)
    timeList.append(eventTime)
newDF = pd.DataFrame(timeList, columns=['EventTime'])
# Replace new dataframe to original dataframe
df.date = newDF.EventTime.values
# change the default name of col
df.rename(columns={"username": "Username", "tweet": "Content", "hashtags": "HashTags", "likes_count": "Likes", "replies_count": "Comments", "retweets_count": "Shares", "date": "EventTime"}, inplace = True)
df.to_csv('DataFromTwitter.csv', index=False, sep=',')
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromTwitter.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromTwitter.csv', index = False)