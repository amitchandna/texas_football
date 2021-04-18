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

url_names = 'https://www.maxpreps.com/rankings/baseball-spring-18/{}/national.htm'
url_scores = 'https://www.maxpreps.com/high-schools/{})/baseball-spring-18/schedule.htm'
url_contact_info = 'https://www.maxpreps.com/high-schools/{})/home.htm'
#state_set = ['california','colorado','illinois','iowa','kentucky','new-hampshire','new-jersey','new-mexico','south-dakota','tennessee']
school_name=[]
#518 pages
for x in tqdm(range(0,2,1)):
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
                    score.append(item.find('span', attrs={'class':'sc-eCssSg claBQF'}).text)
                except:
                    score.append('nan-nan')
                try:
                    away_team.append(item.find('a', attrs={'class':'sc-gsTCUz bSxirR'}).text)
                except:
                    away_team.append(np.nan)
                try:
                    result.append(item.find('span', attrs={'class':'sc-eCssSg eMzzKy'}).text)
                except:
                    result.append("L")
                try:
                    date_of_contest.append(item.find('div', attrs={'class':'sc-eCssSg HzjAa'}).text)
                except:
                    date_of_contest.append(np.nan)
                try:
                    place_played.append(item.find('div', attrs={'class':'sc-eCssSg ccXTnd'}).text)
                except:
                    place_played.append(np.nan)
                try:
                    time_of_contest.append(item.find('div', attrs={'class':'sc-eCssSg cSobln'}).text)
                except:
                    time_of_contest.append(np.nan)
                try:
                    #This is a slight mess, and will need to be cleaned up later - but for now is should be fine....
                    for val in range(1):
                        scores = url_scores.format(name)
                        r = requests.get(scores)
                        soup_1 = BeautifulSoup(r.text,'html.parser')
                        for item in soup_1.find_all('div', attrs={'class':'LayoutManager__StyledLayoutManagerWrapper-sc-1hksfx8-1 ilMntm'}):
                            try:
                                home_team.append(item.find('h1', attrs={'class':'Heading__StyledHeading-sc-1ape2tl-0 ckzGWy'}).text)
                            except:
                                home_team.append(np.nan)
                           # try:
                               # mascot.append(item.find('span', attrs={'class','Text__StyledText-jknly0-0 StyledSchoolHeader__StyledSchoolMascotName-sc-1ps5it5-2 kjABeh jvGvem'}).text)
                           # except:
                               # mascot.append(np.nan)
                except:
                    continue
                try:
                    for x in range(1):
                        contact = url_contact_info.format(name)
                        r = requests.get(contact)
                        soup_2 = BeautifulSoup(r.text,'html.parser')
                        for item in soup_2.find_all('dl', attrs={'class':'SchoolInfo__StyledData-sc-804m01-2 cDIyVj'}):
                            try:
                                address.append(item.find('dd', attrs={'class':'sc-eCssSg ieSBgE'}).text)
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
                
                with open('baseball_boys_1.csv', 'a') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(result)
                    f_object.close()
notify.send('I am finished - come check on me')
