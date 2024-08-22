import scrapy
import pandas as pd
import os
from urllib.parse import urlparse, urlunparse
from Scraper.items import WebItem

class WebsiteSpider(scrapy.Spider):
    name = "websiteSpider"
    allowed_domains = ["insights.blackcoffer.com"]

    def start_requests(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the path to the Excel file
        file_path = os.path.join(current_dir, '..', '..', 'Input.xlsx')
        
        # Load the Excel file with headers
        df = pd.read_excel(file_path, header=0)
        
        # Extract URLs and URL_IDs from the DataFrame
        urls = df.iloc[:, 1].dropna().tolist()  # Drop NaN values and convert to list
        url_ids = df.iloc[:, 0].dropna().tolist()  # Drop NaN values and convert to list
        
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"Number of URLs: {len(urls)}")
        
        for url, url_id in zip(urls, url_ids):
            if not url:
                continue  # Skip empty URLs
            
            # Ensure URL has a scheme
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'http://' + url  # Default to http if scheme is missing
            
            # Ensure URL is absolute
            if not parsed_url.netloc:
                url = urlunparse(('http', url, '', '', '', ''))

            # Pass the URL_ID through the meta attribute
            yield scrapy.Request(url=url, callback=self.parse, meta={'url_id': url_id})

    custom_settings = {
        'FEEDS': {
            'output.csv': {'format': 'csv', 'overwrite': True},
        }
    }

    def parse(self, response):
        web_item = WebItem()
        web_item['url'] = response.url
        web_item['url_id'] = response.meta.get('url_id', '')  # Extract URL_ID from meta data
        
        title = response.css('h1 ::text').get()
        if title:
            title = title.lower()
        else:
            title = 'No title found'
        
        content = " ".join(response.css('div.td-post-content.tagdiv-type ::text').getall())
        web_item['content'] = f"{title} {content}"
        
        yield web_item
