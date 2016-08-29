from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import sys
import utils


def start_link_spider(feed_file, url=None, urls=None):
    settings = get_project_settings()
    settings.set(name='FEED_URI', value=feed_file)
    process = CrawlerProcess(settings)
    process.crawl('link_spider', url=url, urls=urls)
    process.start() 

def start_gallery_spider(cat_id, feed_file, depth):
    settings = get_project_settings()
    settings.set(name='FEED_URI', value=feed_file)
    process = CrawlerProcess(settings)
    process.crawl('gallery_spider', cat_id=cat_id, depth=int(depth))
    process.start()

def galleries2images(in_feed_file, out_feed_file, k=10):
    # gather gallery urls from in_feed_file
    galleries = utils.read_json(in_feed_file)
    # sort and filter
    _galleries = sorted(galleries, key = lambda x : x['score'], reverse=True)[:k]
    print('Number of galleries : ',len(_galleries))
    _galleries = [ item['url'] for item in _galleries ]
    # start link_spider to get images
    start_link_spider(feed_file=out_feed_file, urls=_galleries)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        #start_gallery_spider(cat_id=sys.argv[1],feed_file=sys.argv[2],depth=sys.argv[3])
        #print('\n\n\n-------------------------------------------------------\n\n\n')
        galleries2images(in_feed_file=sys.argv[2], out_feed_file='gallery1.json', k=100)
    print('>> python3 if_link_run.py cat_id feed_file depth')
