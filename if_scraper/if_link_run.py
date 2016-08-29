from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import sys


def start_spider(url,feed_file):
    settings = get_project_settings()
    settings.set(name='FEED_URI', value=feed_file)
    process = CrawlerProcess(settings)
    process.crawl('link_spider', url=url)
    process.start() 

if __name__ == '__main__':
    if len(sys.argv) > 2:
        start_spider(sys.argv[1],sys.argv[2])
