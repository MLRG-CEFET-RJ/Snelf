#import random
from _data_augmentation._log import register_log
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import time
from datetime import datetime
from email.utils import mktime_tz, parsedate_tz


def googleSearch(query, delay):
    #this is the dict we store the search results
    g_clean = {}

    #this is the actual query we are going to scrape
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)

    # exponential factor to delay
    expo_delay = 2

    # max delay
    max_delay = 86400  # 24 hours

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        with requests.get(url, headers=headers) as html:
            while html.status_code!=200:
                # test sleep
                #rand = random.randrange(1,10)
                #if rand==3:
                    #register_log('Sleeping for {} seconds.'.format(rand), print_msg=True)
                    #time.sleep(rand)
                    #register_log('Out of sleep.', print_msg=True)

                # if too many requests was reached, try get "Retry-After" header
                if html.status_code==429:
                    ra = html.headers.get("Retry-After")
                    if ra is not None:
                        if ra.isnumeric():
                            seconds = int(ra)
                        else:
                            today = datetime.today()
                            timestamp = mktime_tz(parsedate_tz(ra))
                            future = datetime.utcfromtimestamp(timestamp)
                            seconds = (future-today).total_seconds()
                    else:
                        seconds = min(delay**expo_delay, max_delay)
                        if seconds < max_delay:
                            expo_delay += 1
                # for any other status_code, set arbitrary time to sleep
                else:
                    seconds = min(delay**expo_delay, max_delay)
                    if seconds < max_delay:
                        expo_delay += 1

                # Sleeping before retrying
                register_log('Html status code: {}'.format(html.status_code), print_msg=True)
                register_log('Headers: {}'.format(html.headers))
                register_log('Text: {}'.format(html.text))
                register_log('Sleeping for {} minutes.'.format(seconds/60), print_msg=True)
                time.sleep(seconds)
                register_log('Out of sleep. Retrying request...', print_msg=True)
                html = requests.get(url, headers=headers)

            # html.status_code is OK (200)
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a') # a is a list
            # [x.get('href') for x in a if x.get('href') is not None and str(x.get('href')).startswith('http')]
            for i in [x for x in a if x.get('href') is not None and str(x.get('href')).startswith('http') and 'google.com' not in str(x.get('href'))]:
                k = i.get('href')

                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if(re.search('google.com', domain.netloc)):
                        continue
                    else:
                        title = i.find('h3').contents[0]
                        # print('*** ', title)
                        title = title.replace('...', '')
                        title = re.sub(' +', ' ', title)
                        g_clean[rul] = title.strip()
                except:
                    continue

    except Exception as ex:
        print('ERROR:', str(ex))

    finally:
        return g_clean