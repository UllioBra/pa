import re,os,time,scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from . import Geturl
from PaBk.items import novelItem

class Pa(scrapy.Spider):
    name = 'pa'
    start_urls = Geturl.Get_Url_List()
            

    def parse(self, response):
        item = novelItem()
        bf = BeautifulSoup(response.text, 'html.parser')
        info = bf.find('div', class_='detail-left').find('div', class_='info')
        item["title"] = info.h1.text
        item["author"] = re.search(r'(?<=val\=)[^(\'|\")]+', str(info)).group()
        item["last_update"] = re.search(r'(?<=>).+更新', str(info)).group()
        item["intro"] = bf.find('p', class_='content intro').text.strip()
        
    