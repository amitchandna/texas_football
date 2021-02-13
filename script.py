#Import statements

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import tqdm
import re
from tqdm import tqdm
from notify_run import Notify

#Setup Web-Notifications

notify = Notify()
notify.register()
print(notify.register())

#Variable names and initialisation

url_names = 'https://www.maxpreps.com/rankings/football-fall-17/{}/state/texas.htm'
url_scores = 'https://www.maxpreps.com/high-schools/{})/football-fall-17/schedule.htm'
url_contact_info = 'https://www.maxpreps.com/high-schools/{})/home.htm'
school_name = []
mascot = []
score = []
home_team = []
away_team = []
date_of_contest = []
result = []
place_played = []
time_of_contest = []
zip_code = []
level = []
season = []
city = []
state = []
address = []
location = []
gender = []
sport = []

#The first of the web scrapers
notify.send('Running the first scraper')

for x in tqdm(range(0,2,1)):
    names = url_names.format(x)
    r = requests.get(names)
    sopa = BeautifulSoup(r.text,'html.parser')
    for item in sopa.find_all('tr'):
        try:
            school_name.append(item.find('th', attrs={'class':'school','scope':'row'}))
        except:
            school_name.append(np.nan)

#Fix the school name tags for use in the new scrapers
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

#Push an update to the web platform
notify.send('I am about to run the main scraper')

#Scraper for Scores - need to parse through the url for each of the schools....
for name in tqdm(my_keys):
        for x in range(1):
            scores = url_scores.format(name)
            r = requests.get(scores)
            soup = BeautifulSoup(r.text,'html.parser')
            #Start to collect the scores:
            for item in soup.find_all('tr'):
                try:
                    score.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 fDENxp'}).text)
                except:
                    score.append('nan-nan')
                try:
                    away_team.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 kLcjsH'}).text)
                except:
                    away_team.append(np.nan)
                try:
                    result.append(item.find('span', attrs={'class':'Text__StyledText-jknly0-0 lkwSff'}).text)
                except:
                    result.append(np.nan)
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
                                mascot.append(item.find('span', attrs={'class','Text__StyledText-jknly0-0 StyledSchoolHeader__StyledSchoolMascotName-sc-1ps5it5-2 kjABeh jvGvem'}))
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
#Time to fix up the scores for something useful!

score_1 = score.copy()
hold_me = []
away_score = []
home_score = []
new_strings = []
win_loss = []
for element in score_1:
    new_string = element.replace("(FF)", "nan-nan")
    new_strings.append(new_string) 
for i in new_strings:
    i = str(i)
    hold_me.append(i.split('-'))    
c = 0
for i in hold_me:
    for s in i:
        c +=1
        if c%2 == 0:
            away_score.append(s)
        else:
            home_score.append(s)
for x,y in zip(home_score,away_score):
    try:
        if int(x) > int(y):
            win_loss.append('Team_1_Win')
        elif int(x) < int(y):
            win_loss.append('Team_1_Loss')
        elif int(x) == int(y):
            win_loss.append('Tie')
    except:
        win_loss.append(np.nan)

#Fix address for address, state, zip:
my_list = []
for element in address:
    element = element.split(", ")
    my_list.append(element)
for i in my_list:
    try:
        location.append(i[0])
    except:
        location.append(np.nan)
    try:
        city.append(i[1])
    except:
        city.append(np.nan)
    try:
        state.append(i[2])
    except:
        state.append(np.nan)
    try:
        zip_code.append(i[3])
    except:
        zip_code.append(np.nan)
for i in range(0,len(home_team),1):
    if len(level) != len(home_team):
        level.append('Varsity')
        season.append('17-18')
        
    else:
        pass
    gender.append('boys')
    sport.append('football')

my_list_1 = []
home_away = []
district = []
for i in place_played:
    i=str(i)
    my_list_1.append(i.split('•'))
for i in my_list_1:
    try:
        home_away.append(i[0])
    except:
        home_away.append(np.nan)
    try:
        district.append(i[1])
    except:
        district.append(np.nan)
#Build up the dataframe now

notify.send('I am about to build the dataframe')
#Might need to split the scores into two different columns..
df = pd.DataFrame()
df = df.transpose()
df['Team_1'] = home_team
df['Team_1_Score'] = home_score
df['Team_1_Zip'] = zip_code
df['Team_2_Team'] = away_team
df['Team_2_Score'] = away_score
df['Sport'] = sport
df['Gender'] = gender
df['Year'] = season
df['Level'] = level
df['City'] = city
df['State'] = state
df['Result'] = win_loss
df['District_Non_District'] = district
df['Away/Home_For_Team_1'] = home_away
df['Date_Of_Contest'] = date_of_contest
df['Time'] = time_of_contest
df.drop_duplicates()
df.dropna()
df.reset_index()

#Finished! Send the csv to a safe location
df.to_csv('max_preps_football_boys_varsity_17_18_texas.csv')
#Let the web notifications know that we are finished here
notify.send('I am finished - come check on me')


