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

url_contact_info = 'https://www.maxpreps.com/high-schools/{})/home.htm'
#state_set = ['california','colorado','illinois','iowa','kentucky','new-hampshire','new-jersey','new-mexico','south-dakota','tennessee']

state_code_list = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy']
# state_code_list = ['az']

school_ids=[]

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        write_obj.close()

schools_indexer = "https://www.maxpreps.com/search/default.aspx?gendersport=girls,swimming&state={}&type=school"
schedule_indexer_a = "https://www.maxpreps.com/local/team/schedule.aspx?schoolid={}&ssid=17fe06a7-c6fb-4850-a717-a3f1d24e9502"
schedule_indexer_b = "https://www.maxpreps.com/local/team/schedule.aspx?schoolid={}&ssid=2d5d410d-095a-499d-a492-4f1d6e516362"
schedule_indexer_c = "https://www.maxpreps.com/local/team/schedule.aspx?schoolid={}&ssid=f8958413-ea44-4cb8-a05c-9c34aeae2915"
for state_code in tqdm(state_code_list):
    school_indexer_url = schools_indexer.format(state_code)
    # print("using school_indexer_url", school_indexer_url)
    r = session.get(school_indexer_url)
    sopa = BeautifulSoup(r.text, 'html.parser')
    # for item in sopa.find_all('li', attrs={'class':'level', 'data-js-jook':'link-varsity','style':''}):
    for item in sopa.find_all('div', attrs={'class':'sport-teams'}):
        # print(item)
        try:
            element = item.find('a')
            # t=(element.text)
            href_tag = element['href']
            # print(element['href'])
            # print(href_tag)
            regex_search = re.search('schoolid=(.*)&gender', element['href']) # look for text inside parens
            # print(item.find('a'))
            # print(regex_search.group(1))
            school_ids.append(regex_search.group(1))
        except:
            element = '' # just need an empty exception

for x in tqdm(school_ids):
    school_schedule_url = schedule_indexer_a.format(x)
    r = session.get(school_schedule_url)
    sopa = BeautifulSoup(r.text, 'html.parser')
    try:
        address = ""
        address_section = sopa.find('address')
        children = address_section.findChildren("span")
        for child in children:
            address = address + str(child.text) + ' '
    except:
        address = np.nan
        continue
    # try:
    #     contact_section = sopa.find('a', attr={'data-lc':'Team-Navigation','data-la':'school-home'})
    #     href_contact_page = contact_section['href']
    #     r = session.get(href_contact_page)
    #     # print("going to find address at ", contact)
    #     soup_2 = BeautifulSoup(r.text,'html.parser')
    #     for item_2 in soup_2.find_all('dl', attrs={'class':'SchoolInfo__StyledData-sc-804m01-2 yPrMn'}):
    #         try:
    #             address=(item_2.find('dd', attrs={'class':'Text__StyledText-g7xgdj-0 eCGytY f16_tall'}).text)
    #         except:
    #             address=('nan,nan,nan,nan')
    # except:
    #     address=('nan,nan,nan,nan')

    try:
        team_1_name = (sopa.find('h1',attrs={'id':'ctl00_NavigationWithContentOverRelated_ContentOverRelated_PageHeaderUserControl_Header'}).text)
        team_1_name = team_1_name[0:team_1_name.find(" 201")]
    except:
        team_1_name = np.nan

    found_table_rows = False
    indexer_index = 'a'
    for schedule_index in range(0, 3, 1):
        table_rows = sopa.find_all('tr', attrs={'class':'dual-contest'})
        print('school ', x, 'with indexer ', indexer_index, ' has ', len(table_rows), ' rows')
        for competition in table_rows:
            found_table_rows = True
            print('found rows with ', indexer_index)
            should_write = True
            try:
                result_score = (competition.find('span', attrs={'class':'score'}).text)
                result_score = result_score.lstrip()
            except:
                result_score= np.nan
                should_write = False
            try:
                date_played = (competition.find('abbr', attrs={'class':'event-date'}).text)
            except:
                date_played= np.nan
                should_write = False
            try:
                time_played = (competition.find('abbr', attrs={'class':'event-time'}).text)
            except:
                time_played = np.nan
                should_write = False
            try:
                team_2_name = (competition.find('a', attrs={'class':'contest-type-indicator contest-type-conference'}).text)
                # try to strip out parens of city state
                team_2_name = re.sub(r'\([^)]*\)', '', team_2_name)
            except:
                try:
                    team_2_name = (competition.find('a', attrs={'class':'contest-type-indicator contest-type-nonconference'}).text)
                    # try to strip out parens of city state
                    team_2_name = re.sub(r'\([^)]*\)', '', team_2_name)
                except:
                    team_2_name = np.nan
                    should_write = False
            try:
                team_2_citystate = (competition.find('span', attrs={'class':'contest-city-state'}).text)
            except:
                team_2_citystate = np.nan
                should_write = False
            try:
                location = (competition.find('div', attrs={'class':'contest-location'}).text)
                location = location[10:]
            except:
                location = np.nan
                should_write = False

            row = [team_1_name,  team_2_name, result_score, date_played, time_played, location, team_2_citystate,  address]
            if should_write:
                append_list_as_row('good_girls_swimming.csv', row)
        if found_table_rows == True:
            break
        if found_table_rows == False and indexer_index == 'b':
            indexer_index = 'c'
            school_schedule_url = schedule_indexer_c.format(x)
            r = session.get(school_schedule_url)
            sopa = BeautifulSoup(r.text, 'html.parser')
        if found_table_rows == False and indexer_index == 'a':
            indexer_index = 'b'
            school_schedule_url = schedule_indexer_b.format(x)
            r = session.get(school_schedule_url)
            sopa = BeautifulSoup(r.text, 'html.parser')
                # TODO finish putting in information and assigning tags/variables.
                # use this page for reference: 

            # https://www.maxpreps.com/local/team/schedule.aspx?schoolid=ff460529-7a6f-407c-a50c-f113563a2420&ssid=e95a611c-e62c-497d-9415-7302cc399a41


#notify.send('I am about to run the main scraper')


#        row = [team_1,  team_2, score, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
#        append_list_as_row('boys_basketball_1_779.csv', row)
#        # with open('volleyball_1.csv', 'a') as f_object:
#        #     writer_object = writer(f_object)
#        #     # zip, city, state, home/away(location)
#        #     row = [score, team_1, team_2, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
#        #     append_list_as_row('volleyball_1.csv', row)
#        #     writer_object.writerow(str(score))
#        #     writer_object.writerow(str(team_1))
#        #     writer_object.writerow(str(team_2))
#        #     writer_object.writerow(str(date_of_contest))
#        #     writer_object.writerow(str(result))
#        #     writer_object.writerow(str(place_played))
#        #     writer_object.writerow(str(time_of_contest))
#        #     writer_object.writerow(str(team_2_city))
#        #     writer_object.writerow(str(team_2_state))
#        #     writer_object.writerow(str(address))
#        #     f_object.close()
#notify.send('I am finished - come check on me')
