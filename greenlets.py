import os
from functools import reduce
import re
import requests
import gevent
import gevent.monkey
from progress import p
from timing import time_it

gevent.monkey.patch_socket()
def all_links(d):
    links = []
    for root, dirs, files in os.walk(d):
        links.extend(list(map(lambda f_name: os.path.join(root, f_name), list(filter(lambda link: link.endswith("html"), files)))))
    return links

def extract_file_links(f_name):
    return re.findall(r'<a [^>]*href\s*=\s*\"([^\"]+)\"[^>]*>', open(f_name, 'r').read())

def extract_files_links(file_list):
    return list(filter(lambda x: x.startswith('http://') or x.startswith('https://'), list(set(reduce(lambda x, y: x + y, list(map(extract_file_links, file_list)), [])))))

@time_it(p)
def invalid_link(link):
    try:
        r = requests.request('HEAD', link)
    except:
        return True
    return r.status_code != 200

def get_invalid_links(links):
    return list(filter(invalid_link, links))

def check_links_in_dir(d):
    files = all_links(d)
    links = extract_files_links(files)
    p.set_count(len(links))
    is_invalid_lets = [gevent.spawn(invalid_link, link) for link in links]
    gevent.wait()
    is_invalid = list(map(lambda x: x.get(), is_invalid_lets))
    if True in is_invalid:
        print("Invalid links:")
        for i, y in enumerate(is_invalid):
            if y:
                print(links[i])


if __name__ == '__main__':
    check_links_in_dir('codescalers.com')
