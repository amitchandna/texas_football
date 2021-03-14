import pandas as pd
import numpy as np
from notify_run import Notify

notify = Notify()
print(notify.register())
notify.send('Running')
df = pd.read_csv('/Users/amitchandna/Documents/Data_Science/Github/tamu_web_scrape/data_files/texas_boys_football_1718.csv', names=["Score", "Team_2", "Result_team_1", "Date","District","Time","Team_1","Team_1_Mascot","Address","Level","Season"])

s = df.Score
a = df.Address
d = df.District
scored = s.str.split('-', expand=True)
addressed= a.str.split(',', expand=True)
districted = d.str.split('•', expand=True)

df = pd.concat([df,scored], axis=1)
df = df.rename(columns={0:'Score_1', 1:'Score_2'})
df = df.drop(columns={'Score', 2})
df = pd.concat([df,addressed], axis=1)
df = df.rename(columns={0:'team_1_physical_Address',1:'team_1_City',2:'team_1_State',3:'Team_1_Zip_code'})
df = df.drop(columns={'Address',4,5})
df = pd.concat([df,districted], axis=1)
df = df.rename(columns={0:"Home_Away", 1:'District_non_district'})
df = df.drop(columns={'District'})
df = df[['Team_1','Score_1', 'Team_2', 'Score_2', 'Result_team_1','Home_Away','Team_1_Mascot','Date','District_non_district','Time','Level','Season', 'team_1_physical_Address','team_1_City','team_1_State','Team_1_Zip_code' ]]
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
    if row['Result_team_1'] == 'W':
        team_1_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
        team_2_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
        continue
    else:
        team_2_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
        team_1_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
        continue
df['Score_1'] = team_1_score
df['Score_2'] = team_2_score
df = df.drop_duplicates()
df.to_csv('texas_football_boys_1718_clean.csv')

notify.send('Finished')


