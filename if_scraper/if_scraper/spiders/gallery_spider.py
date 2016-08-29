import scrapy
from bs4 import BeautifulSoup

import utils
from items import GalleryUrlItem

class GallerySpider(scrapy.Spider):
    name = 'gallery_spider'
    base_url = 'http://imagefap.com'

    def __init__(self, cat_id, depth=2, score_threshold=0.0):
        # add start_url to our seed list
        self.start_urls = [ utils.decorate_search_url(cat_id,i) for i in range(depth) ]
        self.score_threshold = score_threshold

    def parse(self, response):
        # get soup from response
        soup = BeautifulSoup(response.body,'lxml')
        gal_tags = soup.findAll('a', {'class' : 'gal_title'})
        for gal_tag in gal_tags:
            url = self.base_url + gal_tag['href']
            yield scrapy.Request(url, 
                    callback=self.parse_gallery, 
                    meta = {'_url' : url})
        
    def parse_gallery(self,response):
        # get soup
        soup = BeautifulSoup(response.body,'lxml')
        # get index from meta of response
        url = response.meta['_url']
        # get score from soup
        score = utils.get_score(soup)
        if score > self.score_threshold:
            gallery_item = GalleryUrlItem()
            gallery_item['url'] = url
            gallery_item['score'] = score
            yield gallery_item
