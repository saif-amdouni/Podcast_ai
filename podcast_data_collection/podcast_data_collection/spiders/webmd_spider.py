import scrapy
from datetime import datetime
import pandas as pd
import os

class WebMDSpider(scrapy.Spider):
    name = 'webmd'
    start_urls = ['https://www.webmd.com/news/articles']
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.data_folder = 'webmd_data'
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.df = pd.DataFrame(columns=['href', 'title', 'description', 'date'])
        

    def parse(self, response):
        current_date = datetime.today().strftime("%b %d, %Y")
        filename = f"webmd_{current_date}.csv"
        for li in response.css(f'li[data-date="{current_date}"]'):
            extracted_data = {
                'date': current_date,
                'href': "https:"+li.css('a::attr(href)').get(),
                'title': li.css('a span.article-title::text').get(),
                'description': li.css('a p.article-description::text').get()
            }
            yield extracted_data
            self.df = self.df.append(extracted_data, ignore_index=True)
        self.df.to_csv(os.path.join(self.data_folder,filename),sep="|",index=False)
    