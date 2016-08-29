import utils
import os
import sys

from multiprocessing import Pool
import urllib.request as ureq

from if_link_run import start_link_spider

is_json = lambda x : '.json' in x

def fetch_file(image_args):
    try:
        path = image_args['path']
        filename = image_args['filename']
        url = image_args['url']
        return ureq.urlretrieve(url, path + '/' + filename), None
    except Exception as e:
        return None, e

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if not is_json(arg):
            # check if temp.json exists and if so, delete it
            try:
                os.remove('temp.json')
            except OSError:
                pass
            # call the spider
            start_link_spider(feed_file='temp.json', url=arg)
            # set filename to 'temp.json'
            image_list = utils.read_json('temp.json')
        else:
            # read from file
            image_list = utils.read_json(arg)

        # create paths
        paths = set([ image_item['path'] for image_item in image_list ])
        # check if folder exists
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        # create workers
        p = Pool(12)
        # give download jobs to workers
        for i,_ in enumerate(p.imap_unordered(fetch_file,image_list)):
            sys.stderr.write('\rProgress : {0:.2f}%'.format(100.0 * (i+1)/len(image_list)))
        print('')
    else:
        print('>> python3 imagedl [filename.json / http://gallery_url]')
