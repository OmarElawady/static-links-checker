import os
from functools import reduce
import re
import requests
import threading

class Controller:
    def __init__(self):
        self.invalid_links = []
        self.remaining_checks = 0

    def finished_check(self, result, link):
        if result:
            self.invalid_links.append(link)
        
        with self.lock:
            self.remaining_checks -= 1
        
        if not self.remaining_checks:
            self.print_invalid_links()
    
    def set_number_of_links(self, checks):
        self.remaining_checks = checks

    def set_lock(self, lock):
        self.lock = lock

    def print_invalid_links(self):
        print("Invalid links:")
        for link in self.invalid_links:
            print(link)

def all_links(d):
    links = []
    for root, dirs, files in os.walk(d):
        links.extend(list(map(lambda f_name: os.path.join(root, f_name), list(filter(lambda link: link.endswith("html"), files)))))
    return links

def extract_file_links(f_name):
    return re.findall(r'<a [^>]*href\s*=\s*\"([^\"]+)\"[^>]*>', open(f_name, 'r').read())

def extract_files_links(file_list):
    return list(filter(lambda x: x.startswith('http://') or x.startswith('https://'), list(set(reduce(lambda x, y: x + y, list(map(extract_file_links, file_list)), [])))))

def invalid_link(link):
    try:
        r = requests.request('HEAD', link)
    except:
        return True
    return r.status_code != 200

def get_invalid_links(links):
    return list(filter(invalid_link, links))

def reporting_invalid_link(link, func):
    func(invalid_link(link), link)

def check_links_in_dir(d):
    controller = Controller()
    links = (extract_files_links(all_links(d)))
    lock = threading.Lock()
    controller.set_number_of_links(len(links))
    controller.set_lock(lock)
    for link in links:
        t = threading.Thread(target = reporting_invalid_link, args=(link, controller.finished_check))
        t.start()

if __name__ == '__main__':
    check_links_in_dir('codescalers.com')
