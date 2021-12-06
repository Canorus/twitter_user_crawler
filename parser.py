from bs4 import BeautifulSoup as bs
from logg import *
import re

def parse_body(t):
    status_list = list()
    if type(t) == bs:
        t_bs = t
    else:
        try:
            t_bs = bs(t, 'html.parser')
        except:
            logger.error('error occurred while parsing soup')
            return 1
    for article in t_bs.find_all('article'):
        sn = get_sn(article)
        if is_in_history(sn):
            continue
        status = get_status(article)
        if status != None:
            status = clean_(status.get_text()) # status
        else:
            continue
        url_attached = get_link(article) # get attached link
        if url_attached:
            status += '\n' + url_attached
        if len(get_img(article)):
            image_list = get_img(article)
            status += '\n' + ','.join(image_list)
        status_list.append(status)
        logger.debug(status)
        if sn != None:
            print('sn: ', sn)
            add_to_history(sn)
    return status_list

def get_status(t :bs):
    return t.find_all('span')[4]

def clean_(t :str):
    t_s = t.strip().split('\n')
    return ' '.join([x.strip() for x in t_s])

def get_link(t :bs):
    a_list = t.find_all('a')
    for ai in a_list:
        if ai['href'].startswith('http'):
            return ai['href']
    return False

def get_sn(t :bs):
    a_list = t.find_all('a')
    for ai in a_list:
        if not ai['href'].startswith('http') and re.search('\/status\/\d*$', ai['href']):
            logger.debug('sn: ' + ai['href'].split('/')[-1])
            return ai['href'].split('/')[-1]

def add_to_history(s :str):
    logger.debug('add sn to history: ' + s)
    with open(os.path.join(base, 'history.db'), 'a') as fa:
        fa.write('\n' + s)

def read_history():
    if not os.path.exists(os.path.join(base, 'history.db')):
        add_to_history('')
    with open(os.path.join(base, 'history.db')) as f:
        t = [x.strip() for x in f.read().split('\n') if x != '']
    return t

def is_in_history(s :str):
    t = read_history()
    if s in t:
        return True
    else:
        return False

def get_img(t :bs):
    res = list()
    for im in t.find_all('img', attrs={'alt':'Image'}):
        if re.search('/media/.*$', im['src']):
            res.append(re.sub('&.*$', '', im['src']))
    return res
    
