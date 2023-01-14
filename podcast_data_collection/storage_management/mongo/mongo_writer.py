import sys
import os

# get the current directory path
myDir = os.path.dirname(os.path.abspath(__file__))
print(myDir)
sys.path.append(myDir)

import mongoengine as me
from datetime import datetime
# import entity manager
from entity_manager import *
from tqdm import tqdm
import config 
import pandas as pd

class MongoWriter :
    def __init__(self) -> None:
        """
        Initialize the connection to MongoDB and setup the entity manager
        """
        # Connect to MongoDB
        mongoCred = f"mongodb://{config.mongohost}:{config.mongoport}"
        me.connect("Podcast_AI",host = mongoCred)
        # Dictionary to store the methods to process messages based on the topic
        self.messagesProcessors = {"Health" : self.processHealthArticles}
        self.articles_df = None

    def read_articles(self,topic, date):
        """
        Read the articles from csv file
        :param topic: name of the topic
        :param date: date for which the articles needs to be read in the format of 'Month Day, Year'
        """
        self.articles_df = pd.read_csv(f"podcast_data_collection/Data/Data_02/{topic}/{date}.csv",sep="|")
    
    def saveMongo(self, topic) :
        """
        Save the articles to MongoDB
        :param topic: topic of the articles
        """
        print(f"got new {len(self.articles_df)} articles on topic {topic}!")
        if len(self.articles_df)>0:
            self.messagesProcessors[topic]()

    def processHealthArticles(self):
        """
        Process the health articles and save them to MongoDB
        """
        for _,article in tqdm(self.articles_df.iterrows(),total=len(self.articles_df)) :   
            try :
                #get the details from the dataframe
                title = article["title"]
                description = str(article["description"])
                link = article["href"]
                date = article["date"]
                data_source = article["data_source"]
                
            except Exception as e:
                print("article is corrupt !")
                continue
            #save the article to MongoDB
            MedicalArticle(title=title, 
                            description = description, 
                            link=link, 
                            date=date,
                            data_source=data_source).save()
    
if __name__ == "__main__":
    Writer = MongoWriter()
    #read the articles
    Writer.read_articles(topic="Health_Data",date="January 11, 2023")
    # save the articles to MongoDB
    Writer.saveMongo("Health")