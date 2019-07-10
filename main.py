import os
from functools import reduce
import re
def all_links(d):
    links = []
    for root, dirs, files in os.walk(d):
        links.extend(list(map(lambda f_name: os.path.join(root, f_name), list(filter(lambda link: link[-4:] == "html", files)))))
    return links

def extract_file_links(f_name):
    links = []
    return re.findall('<a .*href\s*=\s*[\'"]([^"]+)[\'"].*>', open(f_name, 'r').read())

def extract_files_links(file_list):
    return list(set(reduce(lambda x, y: x + y, list(map(extract_file_links, file_list)), [])))

if __name__ == '__main__':
    import pprint
    pprint.pprint(extract_files_links(all_links('site')))
