import openai
import pymongo
from tqdm import tqdm

class PodcastWriter:
    def __init__(self):
        """
        This is the constructor method that initializes the class by creating a MongoDB client, 
        connecting to a specific database, and initializing the collection of articles. It also sets the OpenAI API key.
        """
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Podcast_AI"]
        self.articles = self.db["medical_article"]
        openai.api_key = "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"
    def get_articles(self):
        """Retrieve articles from the database"""
        return self.articles.find({})
    
    def generate_podcast(self, article):
        """This method takes an article as an input and uses the OpenAI API to generate a podcast script for the article. 
        It creates a prompt with the title, link, and description of the article and sends it to the OpenAI API. 
        It then returns the generated podcast script."""
        prompt = (f"Write a 3 min podcast episode about the following article, the podcast to be friendly and amusing : \n"
                  f"Title: {article['title']} \n"
                  f"Link: {article['link']} \n"
                  f"Description: {article['description']}")
                  
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        return message
    
    def save_podcast(self, article, podcast):
        """This method takes an article and a podcast script as inputs and saves the podcast script 
        in a text file with the name of the article as the file name"""
        with open(f"podcast_data_collection/Data/Data_03/Health_Data/{article['title']}.txt", "w") as file:
            file.write(podcast)
    
    def create_podcasts(self):
        """This method retrieves all articles from the MongoDB collection, generates a podcast script 
        for each article using the generate_podcast() method, and saves the podcast script in a text 
        file using the save_podcast() method. It also uses the tqdm library to display a progress bar 
        while generating the podcasts and prints a message once all podcasts have been generated and 
        saved successfully."""

        articles = self.get_articles()
        for article in tqdm(articles):
            podcast = self.generate_podcast(article)
            self.save_podcast(article=article,podcast=podcast)
        print("All podcasts generated and saved successfully!")
        
if __name__ == "__main__":
    PodcastGen = PodcastWriter()
    PodcastGen.create_podcasts()