import utils

class Gallery(object):

    def __init__(self,base_url):
        self.soup = utils.get_soup(base_url)
        self.title = ''.join(self.soup.title.text.split(' ')[3:])
        self.uploader, self.max_pages, self.score = utils.get_album_params(self.soup)
        self.album_urls = utils.get_album_urls(base_url,self.max_pages)
        self.base_url = base_url

    def __str__(self):
        return '{0} by {1}, rated {2}/10'.format(self.title,self.uploader,self.score)

    def fetch_content(self):
        if self.album_urls:
            self.images = utils.get_all_images(self.album_urls)
        else:
            print('Unable to fetch content : this gallery is empty!')
