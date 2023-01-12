



import scrapy
from datetime import datetime
import pandas as pd
import os

class healthlineSpider(scrapy.Spider):
    name = 'healthline'
    start_urls = ['https://www.healthline.com/health-news']
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.data_folder = 'healthline_data'
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.df = pd.DataFrame(columns=['href', 'title', 'description', 'date'])
        

    def parse(self, response):
        current_date = datetime.today().strftime("%B %d, %Y")
        filename = f"healthline_{current_date}.csv"
        for li in response.css(f'li[class="css-18vzruc"]'):
            article_date = li.css('div.css-mmjpxh::text').get()
            if current_date != article_date :
                break
            extracted_data = {
                # Get the title of the article
                "title": li.css('a h2::text').get(),

                # Get the link of the article
                "href": "https://www.healthline.com"+li.css('a::attr(href)').get(),

                # Get the date of the article
                "date": article_date,

                "description": li.css('p a::text').get()
            }
            yield extracted_data
            self.df = self.df.append(extracted_data, ignore_index=True)
        self.df.to_csv(os.path.join(self.data_folder,filename),sep="|",index=False)
    