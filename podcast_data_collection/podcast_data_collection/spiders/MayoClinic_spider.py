import scrapy
from datetime import datetime
import pandas as pd
import os

class MayoClinicSpider(scrapy.Spider):
    name = "mayo_clinic"
    
    def __init__(self, name=None, **kwargs):

        self.start_urls = ['https://newsnetwork.mayoclinic.org/archive/']
        super().__init__(name, **kwargs)
        self.data_folder = 'MayoClinic_data'
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        self.df = pd.DataFrame(columns=['href', 'title', 'description', 'date'])
    
    def start_requests(self):
        headers = {
            'authority': 'newsnetwork.mayoclinic.org',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7',
            'referer': 'https://newsnetwork.mayoclinic.org/archive/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }

        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
        

    def parse(self, response):
        print(response)
        current_date = datetime.today().strftime("%B %d, %Y")
        filename = f"webmd_{current_date}.csv"
        for article in response.css('div.media-body'):
            # print(article)
            article_date = article.css('div.list-item-meta span.byline-date::text').get()
            if current_date != article_date :
                break
            extracted_data = {
                'href': article.css('div.list-item-title a::attr(href)').get(),
                'title': article.css('div.list-item-title a span::text').get(),
                'description': "",
                # 'description': article.css('div.list-item-content-ch-link-reference::text').get(),
                'date': article_date
            }
            yield extracted_data
            self.df = self.df.append(extracted_data, ignore_index=True)
        self.df.to_csv(os.path.join(self.data_folder,filename),sep="|",index=False)
    