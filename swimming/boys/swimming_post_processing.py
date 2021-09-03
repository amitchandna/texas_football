import pandas as pd
import numpy as np
# from notify_run import Notify

# notify = Notify()
# print(notify.register())
# notify.send('Running')
df = pd.read_csv('~/Documents/texas_football/swimming/boys/boys_swimming.csv', names=["Team_1", "Team_2", "Score", "Date","Time","Location","Team_2_CityState","Team_1_Address"])
# df = pd.read_csv('~/Documents/texas_football/swimming/boys/boys_swimming_header.csv', names=["Team_1", "Team_2", "Score", "Date","Time","Location","Team_2_CityState","Team_1_Address"])

# df = pd.read_csv('/Users/amitchandna/Documents/Data_Science/Github/tamu_web_scrape/data_files/texas_boys_football_1718.csv', names=["Score", "Team_2", "Result_team_1", "Date","District","Time","Team_1","Team_1_Mascot","Address","Level","Season"])
Team_1 = df.Team_1
Team_2 = df.Team_2
Score = df.Score
Date = df.Date
Location = df.Location
Time = df.Time
Team_2_CityState = df.Team_2_CityState
Team_1_Address = df.Team_1_Address

result_list = Score.str.split(' ', expand=True)
team_1_address_list = Team_1_Address.str.split(',', expand=True)
team_1_statezip = team_1_address_list[1].str.split(' ',expand=True)
team_2_citystate_list = Team_2_CityState.str.split(',',expand=True)
team_2_citystate_list[0] = team_2_citystate_list[0].str[1:]
team_2_citystate_list[1] = team_2_citystate_list[1].str[:-1]

df = pd.concat([df, result_list], axis=1)
df = df.rename(columns={0:'Result_Team_1',1:'Score_1',3:'Score_2'})
df = df.drop(columns={'Score',2})
df['Result_Team_1'] = df['Result_Team_1'].str[1:-1]
df = pd.concat([df, team_1_address_list], axis=1)
df = df.rename(columns={0:'Team_1_Street_Address'})
df = df.drop(columns={1})
df = pd.concat([df,team_1_statezip], axis=1)
df = df.rename(columns={1:'Team_1_State',2:'Team_1_Zip'})
df = df.drop(columns={0,3})

street_addresses = []
cities = []
for index,row in df.iterrows():
    street_addresses.append(row['Team_1_Street_Address'][:row['Team_1_Street_Address'].rfind(' ')])
    cities.append(row['Team_1_Street_Address'][row['Team_1_Street_Address'].rfind(' ')+1:])

df['Team_1_Street_Address'] = street_addresses
df = pd.concat([df, pd.Series(cities)], axis=1)
df = df.rename(columns={0:'Team_1_City'})
df = df.drop(columns={'Team_1_Address','Team_2_CityState'})
df = pd.concat([df, team_2_citystate_list],axis=1)
df = df.rename(columns={0:'Team_2_City',1:'Team_2_State'})
df = df[['Team_1', 'Score_1', 'Team_2', 'Score_2', 'Result_Team_1', 'Date', 'Time', 'Location', 'Team_1_Street_Address', 'Team_1_City', 'Team_1_State', 'Team_1_Zip','Team_2_City', 'Team_2_State' ]]

# df = pd.concat([df, score_list], axis=1)
# df = df.rename(columns={0:'Score_1', 1:'Score_2'})
# df = df.drop(columns={'Score'})
# df = pd.concat([df,team_1_address_list], axis=1)
# df = df.rename(columns={0:'Team_1_Street_Address',1:'Team_1_City',2:'Team_1_State',3:'Team_1_Zip'})
# df = df.drop(columns={'Team_1_Address'})
# df = pd.concat([df, districted_list], axis=1)
# df = df.rename(columns={0:'Team_1_Home_Away', 1:'League_District_Nondistrict'})
# df = df.drop(columns={'Location'})
# df = df[['Team_1', 'Score_1', 'Team_2', 'Score_2', 'Result_Team_1', 'Team_1_Home_Away', 'Date', 'Time', 'League_District_Nondistrict', 'Team_1_Street_Address', 'Team_1_City', 'Team_1_State', 'Team_1_Zip', 'Team_2_City', 'Team_2_State']]

# df = pd.concat([df,scored], axis=1)
# df = df.rename(columns={0:'Score_1', 1:'Score_2'})
# df = df.drop(columns={'Score', 2})
# df = pd.concat([df,addressed], axis=1)
# df = df.rename(columns={0:'team_1_physical_Address',1:'team_1_City',2:'team_1_State',3:'Team_1_Zip_code'})
# df = df.drop(columns={'Address',4,5})
# df = pd.concat([df,districted], axis=1)
# df = df.rename(columns={0:"Home_Away", 1:'District_non_district'})
# df = df.drop(columns={'District'})
# df = df[['Team_1','Score_1', 'Team_2', 'Score_2', 'Result_team_1','Home_Away','Team_1_Mascot','Date','District_non_district','Time','Level','Season', 'team_1_physical_Address','team_1_City','team_1_State','Team_1_Zip_code' ]]
team_1_score = []
team_2_score = []
for index,row in df.iterrows():
    if row['Score_1'] == None or row['Score_2'] == None:
        row['Score_1'] = -1
        row['Score_2'] = -2
        continue
    numeric_score = ''
    for element in row['Score_1']:
        if element.isdigit():
            numeric_score += element
    if numeric_score != '':
        row['Score_1'] = int(numeric_score)
    else:
        row['Score_1'] = -3
    numeric_score = ''
    for element in row['Score_2']:
        if element.isdigit():
            numeric_score += element
    if numeric_score != '':
        row['Score_2'] = int(numeric_score)
    else:
        row['Score_2'] = -4

for index,row in df.iterrows():
    if row['Result_Team_1'] == 'W':
        team_1_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
        team_2_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
        continue
    else:
        team_2_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
        team_1_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
        continue
df['Score_1'] = team_1_score
df['Score_2'] = team_2_score
df['Team_2'] = df['Team_2'].str[:-1]
# df['Team_1_Home_Away'] = df['Team_1_Home_Away'].str[:-1]
# df['League_District_Nondistrict'] = df['League_District_Nondistrict'].str[1:]
# df['Team_1_City'] = df['Team_1_City'].str[1:]
df['Team_2_State'] = df['Team_2_State'].str[1:]
# df['Team_1_Zip'] = df['Team_1_Zip'].str[1:]
df = df[df.Score_1 >= 0]
df = df[df.Score_2 >= 0]
df = df.drop_duplicates()
df.to_csv('clean_boys_swimming_1.csv')

# notify.send('Finished')


