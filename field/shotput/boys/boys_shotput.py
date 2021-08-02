from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import requests
import tqdm
import re
from tqdm import tqdm
from notify_run import Notify
import csv
from csv import writer

notify = Notify()
print(notify.register())

# set up retry with backoff bc of maxpreps limiting
session = requests.Session()
retry = Retry(connect=10,total=10, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
# now just use session.get instead of requests.get

url_local_follow = 'https://www.maxpreps.com{}'
url_table = ' https://www.maxpreps.com/leaders/track-field-spring-18/throwing,shot+put/stat-leaders-{}.htm'
#state_set = ['california','colorado','illinois','iowa','kentucky','new-hampshire','new-jersey','new-mexico','south-dakota','tennessee']
school_name=[]

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        write_obj.close()

notify.send('I am about to run the main scraper')
#55 pages
# for x in tqdm(range(0,2,1)):
for x in tqdm(range(0,56,1)):
    table_url = url_table.format(x)
    r = session.get(table_url)
    sopa = BeautifulSoup(r.text,'html.parser')
    for item in sopa.find_all('tr'):
        should_write = True
        try:
            national_ranking = (item.find('td', attrs={'class':'rank first'}).text)
        except:
            national_ranking = np.nan
            should_write = False
        # try:
        #     student_name = (item.find('a', attrs={'href':re.compile('/local/player.*')}).text)
        #     initials = ''.join([char for char in student_name if char.isupper()])
        #     print(initials)
        # except:
        #     student_name = np.nan
        try:
            school_tag = item.find('a', attrs={'class':'team'})
            school_name = (school_tag.text)
            school_name = re.sub(r' \([^)]*\)', '', school_name)
            try:
                school_link = (school_tag['href'])
                follow_school_url = url_local_follow.format(school_link)
                r2 = session.get(follow_school_url)
                address_sopa = BeautifulSoup(r2.text, 'html.parser')
                address = address_sopa.find('address').text
            except:
                address = np.nan
                should_write = False
        except:
            school_name = np.nan
            address = np.nan
            should_write = False
        try:
            date = item.find('span', attrs={'class':'event-date'}).text
        except:
            date = np.nan
            should_write = False
        # try:
        #     wind = item.find('td', attrs={'class':'wind'}).text
        # except:
        #     wind = np.nan
        #     should_write = False
        try:
            result = item.find('td', attrs={'class':'result last'}).text
        except:
            result = np.nan
            should_write = False
        if should_write:
            # row = [school_name, national_ranking, result, wind, date, address]
            row = [school_name, national_ranking, result, date, address]
            append_list_as_row('boys_shotput_1_55.csv', row)
        # print('rank: ', national_ranking, 'name: ', student_name, 'school: ', school_name, 'address: ', address)

        # row = [team_1,  team_2, score, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
        # append_list_as_row('boys_basketball_1_779.csv', row)
notify.send('I am finished - come check on me')
