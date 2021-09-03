import pandas as pd
import numpy as np
# from notify_run import Notify

# notify = Notify()
# print(notify.register())
# notify.send('Running')
df = pd.read_csv('~/Documents/texas_football/field/long_jump/girls/girls_long_jump_1_40.csv', names=['School', 'Rank', 'Distance_String', 'Wind', 'Date', 'Address'])
# df = pd.read_csv('~/Documents/texas_football/field/long_jump/girls/girls_longjump_header.csv', names=['School', 'Rank', 'Distance_String', 'Wind', 'Date', 'Address'])

# df = pd.read_csv('/Users/amitchandna/Documents/Data_Science/Github/tamu_web_scrape/data_files/texas_boys_football_1718.csv', names=["Score", "Team_2", "Result_team_1", "Date","District","Time","Team_1","Team_1_Mascot","Address","Level","Season"])

School = df.School
Rank = df.Rank
Distance_String = df.Distance_String
Wind = df.Wind
Date = df.Date
Address = df.Address

 # Team_1 = df.Team_1
# Team_2 = df.Team_2
# Score = df.Score
# Date = df.Date
# Result_Team_1 = df.Result_Team_1
# Location = df.Location
# Time = df.Time
# Team_2_City = df.Team_2_City
# Team_2_State = df.Team_2_State
# Team_1_Address = df.Team_1_Address

# score_list = Score.str.split('-',expand=True)
# team_1_address_list = Team_1_Address.str.split(',', expand=True)
# districted_list = Location.str.split('•', expand=True)

address_list = Address.str.split(',', expand=True)

# df = pd.concat([df, score_list], axis=1)
# df = df.rename(columns={0:'Score_1', 1:'Score_2'})
# df = df.drop(columns={'Score'})
df = pd.concat([df,address_list], axis=1)
df = df.rename(columns={0:'Street_Address',1:'City',2:'State_Zip'})
df = df.drop(columns={'Address'})
df['State_Zip'] = df['State_Zip'].str[1:]
State_Zip = df.State_Zip
state_zip_list = State_Zip.str.split(' ', expand=True)
df = pd.concat([df, state_zip_list], axis=1)
df = df.rename(columns={0:'State',1:'Zip'})
df = df.drop(columns={'State_Zip'})
# df = pd.concat([df, districted_list], axis=1)
# df = df.rename(columns={0:'Team_1_Home_Away', 1:'League_District_Nondistrict'})
# df = df.drop(columns={'Location'})
dist_pair = Distance_String.str.split(' ',expand=True)
dist_pair[0] = dist_pair[0].str[:-1]
dist_pair[1] = dist_pair[1].str[:-1]
dist_numbers = []
for index,row in dist_pair.iterrows():
    feet = float(row[0])
    feet = feet + float(row[1])/12.0
    dist_numbers.append(feet)
dist_numbers_series = pd.Series(dist_numbers)
df = pd.concat([df, dist_numbers_series], axis=1)
df = df.rename(columns={0:'Distance_Numeric'})
df = df[['School', 'Rank', 'Distance_String', 'Distance_Numeric', 'Wind', 'Date', 'Street_Address', 'City', 'State', 'Zip']]

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
# team_1_score = []
# team_2_score = []
# for index,row in df.iterrows():
#     if row['Score_1'] == None or row['Score_2'] == None:
#         row['Score_1'] = -1
#         row['Score_2'] = -2
#         continue
#     numeric_score = ''
#     for element in row['Score_1']:
#         if element.isdigit():
#             numeric_score += element
#     if numeric_score != '':
#         row['Score_1'] = int(numeric_score)
#     else:
#         row['Score_1'] = -3
#     numeric_score = ''
#     for element in row['Score_2']:
#         if element.isdigit():
#             numeric_score += element
#     if numeric_score != '':
#         row['Score_2'] = int(numeric_score)
#     else:
#         row['Score_2'] = -4

# for index,row in df.iterrows():
#     if row['Result_Team_1'] == 'W':
#         team_1_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
#         team_2_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
#         continue
#     else:
#         team_2_score.append(row["Score_1"] if (row["Score_1"] > row["Score_2"]) else row["Score_2"])
#         team_1_score.append(row["Score_1"] if (row["Score_1"] < row["Score_2"]) else row["Score_2"])
#         continue
# df['Score_1'] = team_1_score
# df['Score_2'] = team_2_score
# df['Team_1'] = df['Team_1'].str[:-1]
# df['Team_1_Home_Away'] = df['Team_1_Home_Away'].str[:-1]
# df['League_District_Nondistrict'] = df['League_District_Nondistrict'].str[1:]



df['City'] = df['City'].str[1:]
# df['Team_1_State'] = df['Team_1_State'].str[1:]
# df['Team_1_Zip'] = df['Team_1_Zip'].str[1:]
df = df.drop_duplicates()
df.to_csv('clean_girls_longjump_1.csv')

# notify.send('Finished')


