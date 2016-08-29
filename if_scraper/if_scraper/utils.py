import os
from bs4 import BeautifulSoup as bsp
import requests
import re

_BASE_URL = 'http://www.imagefap.com'

def get_soup(url):
    # raw content
    content = requests.get(url).content
    # soup
    return bsp(content,"lxml")

# extract score : core function
def re_extract_score(tag_text):
    rate_result = re.search('\d+,\d+',tag_text)
    vote_result = re.search('\(\d+',tag_text)
    
    if rate_result and vote_result:
        return round( float(rate_result.group().replace(',','.')) 
                * float(vote_result.group().replace('(','')) , 1)
    return 0.0

# extract score
def get_score(soup):
    table_tag = soup.find('table', { 'align' : 'center' })
    if table_tag:
        score_tag = table_tag.find('font')
        if score_tag:
            return re_extract_score(score_tag.text)
    return 0.0

# get album parameters
#   returns [ uploader, max_pages, score ]
def get_album_params(soup):
    # find all hyperlinks
    links = soup.findAll('a')
    #uploader_tag = soup.find('font',{'size' : '3'}).text
    #uploader = re_extract_uploader(uploader_tag)
    uploader = ''
    max_pages = get_max_pages(soup)
    return uploader, max_pages, get_score(soup)

def get_album_urls(seed_aurl, max_pages):
    album_urls = []
    for i in range(max_pages):
        aurl_i = decorate_album_url(seed_aurl,i)
        soup = get_soup(str(aurl_i))
        for item in soup.findAll('a'):
            if 'alt' in str(item) and 'imagefap.com' not in str(item):
                album_urls.append(item['href'])
                break
    return album_urls

def get_max_pages(soup):
    # get soup
    items = soup.findAll('a',{'class' : 'link3'})
    pages = []
    for item in items:
        if 'next' not in item.string and 'prev' not in item.string and item.string:
            if int(item.string) not in pages:
                pages.append(int(item.string))
    if not pages:
        return 1

    return max(pages)

def get_page_images(album_url):
    # get soup
    soup = get_soup(_BASE_URL + album_url)
    image_links = []
    for url in soup.findAll('a'):
        if 'imagefapusercontent' in str(url):
            image_links.append(url['href'])
    # return image_links
    return image_links

def get_all_images(album_urls):
    images = []
    for album_url in album_urls:
        images.extend(get_page_images(album_url))
    return images

# Link Decorator functions
def util_strip_album_url(album_url):
    return album_url[:album_url.find('&page')]

def decorate_album_url(album_url,pid):
    return '{0}&page={1}&view=0'.format(album_url,pid)

def decorate_search_url(cat_id,page):
    ##
    # 'http://www.imagefap.com/gallery.php?type=1&gen=54&userid=&search=&page=1000'
    ##
    base_url_head = 'http://www.imagefap.com/gallery.php?type=1&gen='
    base_url_tail = '&userid=&search=&page='
    return base_url_head + str(cat_id) + base_url_tail + str(page)

def get_base_name(url):
    return os.path.basename(url).replace('/','')
