from bs4 import BeautifulSoup
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

url_names = 'https://www.maxpreps.com/rankings/football-fall-17/{}/state/.htm'
url_scores = 'https://www.maxpreps.com/high-schools/{})/football-fall-17/schedule.htm'
url_contact_info = 'https://www.maxpreps.com/high-schools/{})/home.htm'
#state_set = ['california','colorado','illinois','iowa','kentucky','new-hampshire','new-jersey','new-mexico','south-dakota','tennessee']
school_name=[]

for x in tqdm(range(0,50,1)):
    names = url_names.format(x)
    r = requests.get(names)
    sopa = BeautifulSoup(r.text,'html.parser')
    for item in sopa.find_all('tr'):
        try:
            school_name.append(item.find('th', attrs={'class':'school','scope':'row'}))
        except:
            school_name.append(np.nan)
new_list = []
for i in school_name:
    i = str(i)
    count = 0
    for char in i:
        if char == '/':
            count +=1
        elif count == 2:
            new_list.append(char)
big_string = ''.join(new_list)
my_keys = big_string.split(')')

notify.send('I am about to run the main scraper')

#Scraper for Scores - need to parse through the url for each of the schools....
for name in tqdm(my_keys):
        for x in range(1):
            scores = url_scores.format(name)
            r = requests.get(scores)
            soup = BeautifulSoup(r.text,'html.parser')
            #Start to collect the scores:
            for item in soup.find_all('tr'):
                mascot, score,home_team,away_team, date_of_contest,result,place_played,time_of_contest,zip_code,level,season,city,state,address,location,gender,sport = ([], )*17
                try:
                    score.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 fDENxp'}).text)
                except:
                    score.append('nan-nan')
                try:
                    away_team.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 kLcjsH'}).text)
                except:
                    away_team.append(np.nan)
                try:
                    result.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 jDyzbz'}).text)
                except:
                    result.append("L")
                try:
                    date_of_contest.append(item.find('div', attrs={'class':'Text__StyledText-jknly0-0 iYZphi'}).text)
                except:
                    date_of_contest.append(np.nan)
                try:
                    place_played.append(item.find('div', attrs={'class':'Text__StyledText-jknly0-0 bojGpz'}).text)
                except:
                    place_played.append(np.nan)
                try:
                    time_of_contest.append(item.find('div', attrs={'class':'Text__StyledText-jknly0-0 bgvugT'}).text)
                except:
                    time_of_contest.append(np.nan)
                try:
                    for val in range(1):
                        scores = url_scores.format(name)
                        r = requests.get(scores)
                        soup_1 = BeautifulSoup(r.text,'html.parser')
                        for item in soup_1.find_all('div', attrs={'class':'GlobalHeader__StyledGlobalHeader-zso49d-0 kttgZd'}):
                            try:
                                home_team.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 gYuHkw'}).text)
                            except:
                                home_team.append(np.nan)
                            try:
                                mascot.append(item.find('span', attrs={'class','Text__StyledText-jknly0-0 StyledSchoolHeader__StyledSchoolMascotName-sc-1ps5it5-2 kjABeh jvGvem'}).text)
                            except:
                                mascot.append(np.nan)
                except:
                    continue
                try:
                    for x in range(1):
                        contact = url_contact_info.format(name)
                        r = requests.get(contact)
                        soup_2 = BeautifulSoup(r.text,'html.parser')
                        for item in soup_2.find_all('dl', attrs={'class':'SchoolInfo__StyledData-sc-804m01-2 cDIyVj'}):
                            try:
                                address.append(item.find('dd', attrs={'class':'Text__StyledText-jknly0-0 kGkAlE'}).text)
                            except:
                                address.append('nan,nan,nan,nan')
                except:
                    continue
                try:
                    for x in range(1):
                        scores = url_scores.format(name)
                        r = requests.get(scores)
                        soup_1 = BeautifulSoup(r.text,'html.parser')
                        for item in soup_1.find_all('div', attrs={'class':'sticky-inner-wrapper','style':'position:relative;top:0px;z-index:100'}):
                            try:
                                level.append('Varsity')
                            except:
                                level.append(np.nan)
                            try:
                                season.append('17-18')
                            except:
                                season.append(np.nan)
                except:
                    continue
                
                with open('usa_1.csv', 'a') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(result)
                    f_object.close()
notify.send('I am finished - come check on me')
