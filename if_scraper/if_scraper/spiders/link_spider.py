import scrapy
from bs4 import BeautifulSoup

import utils

class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    start_urls = []

    def __init__(self, url=None, urls=None):
        # add start_url to our seed list
        if url:
            self.start_urls.append(url)
        else:
            self.start_urls = urls

    def parse(self, response):
        # get soup from response
        soup = BeautifulSoup(response.body,'lxml')
        # get title from soup
        self.title = ' '.join(soup.title.text.split(' ')[3:]).replace('/','_')
        # get album params
        _, max_pages, score = utils.get_album_params(soup)
        # get album urls
        # album_urls = utils.get_album_urls(response.url,max_pages)
        for i in range(max_pages):
            aurl_i = utils.decorate_album_url(response.url,i)
            yield scrapy.Request(aurl_i, callback=self.parse_temp_url,
                    meta = {'_index' : i})
        
    def parse_temp_url(self,response):
        # get soup
        soup = BeautifulSoup(response.body,'lxml')
        i = response.meta['_index']
        for item in soup.findAll('a'):
            if 'alt' in str(item) and 'imagefap.com' not in str(item):
                return scrapy.Request('http://imagefap.com' + item['href'], 
                        callback=self.parse_album_url, meta = {'_index' : i})

    def parse_album_url(self,response):
        # get soup
        soup = BeautifulSoup(response.body,'lxml')
        # get index from meta of response
        i = response.meta['_index']
        for j,img_tag in enumerate(soup.findAll('a')):
            if 'imagefapusercontent' in str(img_tag):
                img_url = img_tag.get('href')
                yield { 
                        'path' : self.title, 
                        'filename' : '{0}_{1}_{2}'.format(i,j,utils.get_base_name(img_url)),
                        'url' : img_url
                        }
