from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import os
from time import sleep
from logg import *
from parser import *
import sys

base = os.path.join(os.path.dirname(os.path.abspath(__file__)),'')

def run_selenium():
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/7.0.4 Mobile/16B91 Safari/605.1.15"
    #options = webdriver.FirefoxOptions()
    options = webdriver.ChromeOptions()
    options.headless = True #options.add_argument('--headless')
    options.add_argument('--window-size=1080,3840')
    options.add_argument('user-agent=' + user_agent)
    # decide where geckodriver is based on system name
    system = os.name
    if system == 'posix':
        sysname = os.uname().sysname
    else:
        sysname = 'win'
    if os.uname().nodename == 'raspberrypi':
        logger.debug(os.uname().nodename)
        browser = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    elif sysname == 'Linux':
        logger.debug(sysname)
        browser = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    elif sysname == 'Darwin':
        logger.debug(sysname)
        browser = webdriver.Chrome(
            executable_path='/usr/local/bin/chromedriver', options=options)
    else:
        logger.debug('windows')
        browser = webdriver.Chrome(base + 'chromedriver', options=options)
    return browser

def get_page(browser, url):
    browser.get(url)
    sleep(5)
    #with open('sample.html', 'w') as fw:
    #    fw.write(browser.page_source)

def browser_close(browser):
    browser.close()

if __name__=='__main__':
    browser = run_selenium()
    url = sys.argv[1] # change this part for diff url
    get_page(browser, url)
    status_list = parse_body(browser.page_source)
    browser_close(browser)
