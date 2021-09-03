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

url_names = 'https://www.maxpreps.com/rankings/baseball-spring-18/{}/national.htm'
url_scores = 'https://www.maxpreps.com/high-schools/{})/baseball-spring-18/schedule.htm'
url_contact_info = 'https://www.maxpreps.com/high-schools/{})/home.htm'
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

#518 pages
for x in tqdm(range(518,519,1)):
    names = url_names.format(x)
    r = session.get(names)
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
    scores = url_scores.format(name)
    r = session.get(scores)
    soup = BeautifulSoup(r.text,'html.parser')
    # print(scores)
    try:
        team_1=(soup.find('h1', attrs={'class':'Heading__StyledHeading-sc-1ape2tl-0 kYQvou f28_heavy'}).text)
        team_1 = team_1[0:team_1.find("Baseba")-1]
        # team_1= name[0:name.find('(')-1] # this works ok, not capitalized though
        # team_1 = name
        # bf = item.find('h1', attrs={'class': 'ckzGWy'})
        # print("got a team 1")
    except:
        team_1=(np.nan)
    #Start to collect the scores:
    try:
        contact = url_contact_info.format(name)
        r = session.get(contact)
        # print("going to find address at ", contact)
        soup_2 = BeautifulSoup(r.text,'html.parser')
        for item_2 in soup_2.find_all('dl', attrs={'class':'SchoolInfo__StyledData-sc-804m01-2 yPrMn'}):
            try:
                address=(item_2.find('dd', attrs={'class':'Text__StyledText-g7xgdj-0 eCGytY f16_tall'}).text)
            except:
                address=('nan,nan,nan,nan')
    except:
        address=('nan,nan,nan,nan')
        # continue 
    for item in soup.find_all('tr'):
        #mascot,score,team_1, away_team,date_of_contest,result,place_played,time_of_contest,zip_code,city,state, team_2_city, team_2_state, address,location,gender,sport = ([], )*19
        # address=('nan,nan,nan,nan')
        try:
            score = (item.find('span', attrs={'class':'Text__StyledText-g7xgdj-0 ipvVIk'}).text)
        except:
            score = ('nan-nan')
            # TODO Assign the scores to the teams Post processing properly
        try:
            # here is wherer we need to strip the href out of the tag to get away team city
            element = item.find('a', attrs={'class':'StyledAnchor-sc-14cqspo-0 fAexHO'})
            team_2=(element.text)
            #href_tag = element['href']
            # print(element['href'])
            away_location_pair = re.search('\((.*)\)', element['href']) # look for text inside parens
            # print(away_location_pair.group(1).split(','))
            team_2_city=(away_location_pair.group(1).split(',')[0])
            team_2_state=(away_location_pair.group(1).split(',')[1]).upper()
        except:
            team_2=(np.nan)
            team_2_city=(np.nan)
            team_2_state=(np.nan)
        try:
            # print(item)
            result=(item.find('span', attrs={'class':'Text__StyledText-g7xgdj-0 byvOZr'}).text) # win stylization
        except: # the loss stylization is of class type sc-eCssSg  dyMwZa. if they don't have win, it's a loss
            try:
                result=(item.find('span', attrs={'class':'Text__StyledText-g7xgdj-0 ddInom'}).text) # loss stylization
            except:
                try:
                    result=(item.find('span', attrs={'class':'Text__StyledText-g7xgdj-0 jboaTf'}).text) # actual tie stylization
                except:
                    result=("NoScoreReported")
        try:
            date_of_contest=(item.find('div', attrs={'class':'Text__StyledText-g7xgdj-0 eHnusR f16_bold_tall'}).text)
        except:
            date_of_contest=(np.nan)
        try:
            place_played=(item.find('div', attrs={'class':'Text__StyledText-g7xgdj-0 itManz f14_tall'}).text)
        except:
            place_played=(np.nan)
        try:
            time_of_contest=(item.find('div', attrs={'class':'Text__StyledText-g7xgdj-0 eHnusR f14_tall'}).text)
        except:
            time_of_contest=(np.nan)
                   # try:
                       # mascot=(item.find('span', attrs={'class','Text__StyledText-jknly0-0 StyledSchoolHeader__StyledSchoolMascotName-sc-1ps5it5-2 kjABeh jvGvem'}).text)
                   # except:
                       # mascot=(np.nan)
        # try:
        #     for x in range(1):
        #         contact = url_contact_info.format(name)
        #         r = session.get(contact)
        #         soup_2 = BeautifulSoup(r.text,'html.parser')
        #         for item_2 in soup_2.find_all('dl', attrs={'class':'SchoolInfo__StyledData-sc-804m01-2 yPrMn'}):
        #             try:
        #                 address=(item_2.find('dd', attrs={'class':'Text__StyledText-g7xgdj-0 cjPYhL'}).text)
        #             except:
        #                 address=('nan,nan,nan,nan')
        # except:
        #     address=('nan,nan,nan,nan')
        #     # continue 

        #try:
        #    # grab the anchor that links to the box score
        #    element = item.find("a", attrs={'class':'fKwvDC'})
        #    href_tag = element['href']
        #    # print("element: " , element)
        #    # print("going to get url: ", href_tag)
        #    box_score_r = session.get(href_tag)
        #    box_score_soup = BeautifulSoup(box_score_r.text, 'html.parser')
        #    team_alpha = box_score_soup.find('tr', attrs={'class':'first'})
        #    team_beta = box_score_soup.find('tr', attrs={'class':'last alternate'})

        #    # alpha_scores = [np.nan, np.nan, np.nan, np.nan, np.nan]
        #    alpha_scores = []
        #    # alpha_score_idx = 0
        #    # this gets all the td elements
        #    for score_a in team_alpha.find_all('td'):
        #        # alpha_scores[alpha_score_idx] = int(score_a.text)
        #        # sometimes the text will be a '-' bc it's not available. the int conversion will fail
        #        # and the score list will be nan. 
        #        alpha_scores.append(int(score_a.text))
        #        # alpha_score_idx = alpha_score_idx + 1
        #    # but it also includes the number of games won. get rid of that
        #    # alpha_game_wins = alpha_scores[alpha_score_idx-1]
        #    # alpha_game_wins = alpha_scores[len(alpha_scores)-1]
        #    alpha_game_wins = alpha_scores.pop()
        #    # alpha_scores[alpha_score_idx] = np.nan
        #    # print(alpha_scores)
        #    # print(alpha_game_wins)

        #    # beta_scores = [np.nan, np.nan, np.nan, np.nan, np.nan]
        #    beta_scores = []
        #    # beta_score_idx = 0
        #    # this gets all the td elements
        #    for score_a in team_beta.find_all('td'):
        #        # beta_scores[beta_score_idx] = int(score_a.text)
        #        beta_scores.append(int(score_a.text))
        #        # beta_score_idx = beta_score_idx + 1
        #    # but it also includes the number of games won. get rid of that
        #    # beta_game_wins = beta_scores[beta_score_idx-1]
        #    # beta_game_wins = beta_scores[len(beta_scores)-1]
        #    beta_game_wins = beta_scores.pop()
        #    # beta_scores[beta_score_idx] = np.nan
        #    # print(beta_scores)
        #    # print(beta_game_wins)

        #    # # this gets all the td elements
        #    # beta_scores = [np.nan, np.nan, np.nan, np.nan, np.nan]
        #    # beta_score_idx = 0
        #    # for score_a in team_beta.find_all('td'):
        #    #     beta_scores[beta_score_idx] = int(score_a.text)
        #    #     beta_score_idx = beta_score_idx + 1
        #    # # but it also includes the number of games won. get rid of that
        #    # beta_game_wins = beta_scores[beta_score_idx-1]
        #    # beta_scores[beta_score_idx] = np.nan

        #    if(beta_game_wins > alpha_game_wins):
        #        #  here team_beta is the winner
        #        if(result == 'W'):
        #            # team beta is team 1
        #            team_2_score_list = alpha_scores
        #            team_1_score_list = beta_scores
        #            team_1_games_won = beta_game_wins
        #            team_2_games_won = alpha_game_wins
        #        elif(result == 'L'):
        #            # team beta is team 2
        #            team_1_score_list = alpha_scores
        #            team_2_score_list = beta_scores
        #            team_2_games_won = beta_game_wins
        #            team_1_games_won = alpha_game_wins
        #        else:
        #            print('Result bad')
        #    elif(beta_game_wins < alpha_game_wins):
        #        #  here team_beta is the loser
        #        if(result == 'W'):
        #            # team beta is team 2
        #            team_1_score_list = alpha_scores
        #            team_2_score_list = beta_scores
        #            team_2_games_won = beta_game_wins
        #            team_1_games_won = alpha_game_wins
        #        elif(result == 'L'):
        #            # team beta is team 1
        #            team_2_score_list = alpha_scores
        #            team_1_score_list = beta_scores
        #            team_1_games_won = beta_game_wins
        #            team_2_games_won = alpha_game_wins
        #        else:
        #            print('Result bad')
        #            team_2_score_list = np.nan
        #            team_1_score_list = np.nan
        #            team_1_games_won  = np.nan
        #            team_2_games_won  = np.nan

        #    else:
        #        print("tie game, team_a: ", alpha_game_wins, " beta: " , beta_game_wins)
        #        # whose scores are whose? does it matter since they're the same game wins? could search for other data and match lowercase string names
        #        team_1_score_list = alpha_scores
        #        team_2_score_list = beta_scores
        #        team_2_games_won = beta_game_wins
        #        team_1_games_won = alpha_game_wins

        #    # print("team_alpha: ", alpha_scores, "\nteam_beta: ", beta_scores)
        #    # in the soup we are looking for <tr class="first"> which has children <td class="game1 score dw">, <td class="game2 score dw"> etc for however many games
        #    # then we look for a <tr class="last alternate"> which has the same kinds of children. yoink these scores outta there!

        #    # print(element['href'])
        #except:
        #    # print('it no worky')
        #    alpha_scores = np.nan
        #    beta_scores = np.nan
        #    team_1_score_list = np.nan
        #    team_2_score_list = np.nan
        #    team_1_games_won = np.nan
        #    team_2_games_won = np.nan
        #    #append np.nan to all the individual_game_scores

        #at this point we need to follow the 'box score' link and scrape the game scores for each set. instead of just 3-0, we need to find that team 1 scored [25, 25, 25] points in the sets, team 2 score [8, 19, 11]
        # row = [score, team_1, team_2, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
        # append_list_as_row('volleyball_1.csv', row)
        # print(str(score))
        # print("team1: ", str(team_1)) # all nan
        # print("team1 games: ", str(team_1_games_won))
        # print("team1 list ", str(team_1_score_list))
        # print("team2: ", str(team_2))
        # print("team2 games: ", str(team_2_games_won))
        # print("team2 list ", str(team_2_score_list))
        # print("date: ",str(date_of_contest))
        # print("team1 result: ",str(result))
        # print("place_played: ",str(place_played))
        # print("time: ",str(time_of_contest))
        # print("team 2 city: ", str(team_2_city))
        # print("team 2 state: ", str(team_2_state))
        # print("team 1 addr: ", str(address))
        # print("=======")

        row = [team_1,  team_2, score, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
        append_list_as_row('boys_baseball_518.csv', row)
        # with open('volleyball_1.csv', 'a') as f_object:
        #     writer_object = writer(f_object)
        #     # zip, city, state, home/away(location)
        #     row = [score, team_1, team_2, date_of_contest, result, place_played, time_of_contest, team_2_city, team_2_state, address]
        #     append_list_as_row('volleyball_1.csv', row)
        #     writer_object.writerow(str(score))
        #     writer_object.writerow(str(team_1))
        #     writer_object.writerow(str(team_2))
        #     writer_object.writerow(str(date_of_contest))
        #     writer_object.writerow(str(result))
        #     writer_object.writerow(str(place_played))
        #     writer_object.writerow(str(time_of_contest))
        #     writer_object.writerow(str(team_2_city))
        #     writer_object.writerow(str(team_2_state))
        #     writer_object.writerow(str(address))
        #     f_object.close()
notify.send('I am finished - come check on me')
