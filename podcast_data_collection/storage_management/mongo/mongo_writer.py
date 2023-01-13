import sys
import os

myDir = os.path.dirname(os.path.abspath(__file__))
print(myDir)
sys.path.append(myDir)

import mongoengine as me
from datetime import datetime
from entity_manager import *
from tqdm import tqdm
import config 
import pandas as pd

class MongoWriter :
    def __init__(self) -> None:
        mongoCred = f"mongodb://{config.mongohost}:{config.mongoport}"
        me.connect("Podcast_AI",host = mongoCred)
        self.messagesProcessors = {"Health" : self.processHealthArticles}
        self.articles_df = None

    def read_articles(self,topic, date):
        self.articles_df = pd.read_csv(f"podcast_data_collection/Data/Data_02/{topic}/{date}.csv",sep="|")
    
    def saveMongo(self, topic) :
        print(f"got new {len(self.articles_df)} articles on topic {topic}!")
        if len(self.articles_df)>0:
            self.messagesProcessors[topic]()

    def processHealthArticles(self):
        for _,article in tqdm(self.articles_df.iterrows(),total=len(self.articles_df)) :   
            try :
                title = article["title"]
                description = str(article["description"])
                link = article["href"]
                date = article["date"]
                data_source = article["data_source"]
                
            except Exception as e:
                print("article is corrupt !")
                continue
            MedicalArticle(title=title, 
                            description = description, 
                            link=link, 
                            date=date,
                            data_source=data_source).save()
    
if __name__ == "__main__":
    Writer = MongoWriter()
    Writer.read_articles(topic="Health_Data",date="January 11, 2023")
    Writer.saveMongo("Health")