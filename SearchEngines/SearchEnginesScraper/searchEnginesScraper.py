from search_engines.engines.yahoo import Yahoo
from search_engines.engines.startpage import Startpage
from search_engines.engines.bing import Bing
from search_engines.engines.ask import Ask
from search_engines.engines.aol import Aol
from search_engines.engines.google import Google
import pandas as pd



engine = Google()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromGoogle")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromGoogle.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromGoogle.csv', index = False)

engine = Yahoo()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromYahoo")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromYahoo.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromYahoo.csv', index = False)

engine = Bing()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromBing")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromBing.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromBing.csv', index = False)

engine = Startpage()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromStartpage")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromStartpage.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromStartpage.csv', index = False)

engine = Aol()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromAol")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromAol.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromAol.csv', index = False)

engine = Ask()
results = engine.search("clickshare")
engine.output(output="out.CSV",
              path="DataFromAsk")
# sort the csv via timestamp 
csvData = pd.read_csv("DataFromAsk.csv")
csvData.sort_values(["EventTime"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
csvData.to_csv('DataFromAsk.csv', index = False)