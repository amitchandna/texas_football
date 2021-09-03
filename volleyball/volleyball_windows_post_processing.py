import pandas as pd
import numpy as np
# from notify_run import Notify

# notify = Notify()
# print(notify.register())
# notify.send('Running')
df = pd.read_csv('~/Documents/texas_football/volleyball/full_volleyball_windows.csv', names=["Team_1", "Team_1_Games_Won", "Team_1_Games_List", "Team_2", "Team_2_Games_Won", "Team_2_Games_List", "Date","Result_Team_1","Location","Time","Team_2_City","Team_2_State","Team_1_Address"])
# df = pd.read_csv('~/Documents/texas_football/soccer/girls/girls_soccer_header.csv', names=["Team_1", "Team_2", "Score", "Date","Result_Team_1","Location","Time","Team_2_City","Team_2_State","Team_1_Address"])

# df = pd.read_csv('/Users/amitchandna/Documents/Data_Science/Github/tamu_web_scrape/data_files/texas_boys_football_1718.csv', names=["Score", "Team_2", "Result_team_1", "Date","District","Time","Team_1","Team_1_Mascot","Address","Level","Season"])
# Team_1 = df.Team_1
# Team_2 = df.Team_2
# Score = df.Score
# Date = df.Date
# Result_Team_1 = df.Result_Team_1
Location = df.Location
# Time = df.Time
# Team_2_City = df.Team_2_City
# Team_2_State = df.Team_2_State
Team_1_Address = df.Team_1_Address
Team_1_Games_Won = df.Team_1_Games_Won
Team_2_Games_Won = df.Team_2_Games_Won

df['Team_1_Games_List'] = df['Team_1_Games_List'].str[1:-1]
df['Team_2_Games_List'] = df['Team_2_Games_List'].str[1:-1]
Team_1_Games_List = df.Team_1_Games_List
Team_2_Games_List = df.Team_2_Games_List

team_1_games_array = Team_1_Games_List.str.split(',',expand=True)
team_2_games_array = Team_2_Games_List.str.split(',',expand=True)

team_1_address_list = Team_1_Address.str.split(',', expand=True)
districted_list = Location.str.split(' ', expand=True)


df = pd.concat([df, team_1_games_array], axis=1)
df = df.rename(columns={0:'Team_1_Game_1_Score',1:'Team_1_Game_2_Score',2:'Team_1_Game_3_Score',3:'Team_1_Game_4_Score',4:'Team_1_Game_5_Score'})
df = df.drop(columns={'Team_1_Games_List'})
df = pd.concat([df, team_2_games_array], axis=1)
df = df.rename(columns={0:'Team_2_Game_1_Score',1:'Team_2_Game_2_Score',2:'Team_2_Game_3_Score',3:'Team_2_Game_4_Score',4:'Team_2_Game_5_Score'})
df = df.drop(columns={'Team_2_Games_List'})
df = pd.concat([df, districted_list], axis=1)
df = df.rename(columns={0:'Team_1_Home_Away', 2:'League_District_Nondistrict'})
df = df.drop(columns={'Location',1,3})
df = pd.concat([df,team_1_address_list], axis=1)
df = df.rename(columns={0:'Team_1_Street_Address',1:'Team_1_City',2:'Team_1_State',3:'Team_1_Zip'})
df = df.drop(columns={'Team_1_Address',4,5,6})

# df = pd.concat([df, score_list], axis=1)
# df = df.rename(columns={0:'Score_1', 1:'Score_2'})
# df = df.drop(columns={'Score'})
# df = pd.concat([df,team_1_address_list], axis=1)
# df = df.rename(columns={0:'Team_1_Street_Address',1:'Team_1_City',2:'Team_1_State',3:'Team_1_Zip'})
# df = df.drop(columns={'Team_1_Address'})
# df = pd.concat([df, districted_list], axis=1)
# df = df.rename(columns={0:'Team_1_Home_Away', 1:'League_District_Nondistrict'})
# df = df.drop(columns={'Location'})

try:
    df = df[['Team_1', 'Team_1_Games_Won', 'Team_1_Game_1_Score', 'Team_1_Game_2_Score', 'Team_1_Game_3_Score', 'Team_1_Game_4_Score', 'Team_1_Game_5_Score', 'Team_2', 'Team_2_Games_Won', 'Team_2_Game_1_Score', 'Team_2_Game_2_Score', 'Team_2_Game_3_Score', 'Team_2_Game_4_Score', 'Team_2_Game_5_Score', 'Result_Team_1', 'Team_1_Home_Away', 'League_District_Nondistrict', 'Date', 'Time', 'Team_2_City', 'Team_2_State', 'Team_1_Street_Address', 'Team_1_City', 'Team_1_State', 'Team_1_Zip']]
    df['Team_1_Game_1_Score'] = df['Team_1_Game_1_Score'].str.lstrip()
    df['Team_1_Game_2_Score'] = df['Team_1_Game_2_Score'].str.lstrip()
    df['Team_1_Game_3_Score'] = df['Team_1_Game_3_Score'].str.lstrip()
    df['Team_1_Game_4_Score'] = df['Team_1_Game_4_Score'].str.lstrip()
    df['Team_1_Game_5_Score'] = df['Team_1_Game_5_Score'].str.lstrip()
    df['Team_2_Game_1_Score'] = df['Team_2_Game_1_Score'].str.lstrip()
    df['Team_2_Game_2_Score'] = df['Team_2_Game_2_Score'].str.lstrip()
    df['Team_2_Game_3_Score'] = df['Team_2_Game_3_Score'].str.lstrip()
    df['Team_2_Game_4_Score'] = df['Team_2_Game_4_Score'].str.lstrip()
    df['Team_2_Game_5_Score'] = df['Team_2_Game_5_Score'].str.lstrip()
except:
    df = df[['Team_1', 'Team_1_Games_Won', 'Team_1_Game_1_Score', 'Team_1_Game_2_Score', 'Team_1_Game_3_Score', 'Team_2', 'Team_2_Games_Won', 'Team_2_Game_1_Score', 'Team_2_Game_2_Score', 'Team_2_Game_3_Score', 'Result_Team_1', 'Team_1_Home_Away', 'League_District_Nondistrict', 'Date', 'Time', 'Team_2_City', 'Team_2_State', 'Team_1_Street_Address', 'Team_1_City', 'Team_1_State', 'Team_1_Zip']]
    df['Team_1_Game_1_Score'] = df['Team_1_Game_1_Score'].str.lstrip()
    df['Team_1_Game_2_Score'] = df['Team_1_Game_2_Score'].str.lstrip()
    df['Team_1_Game_3_Score'] = df['Team_1_Game_3_Score'].str.lstrip()
    df['Team_2_Game_1_Score'] = df['Team_2_Game_1_Score'].str.lstrip()
    df['Team_2_Game_2_Score'] = df['Team_2_Game_2_Score'].str.lstrip()
    df['Team_2_Game_3_Score'] = df['Team_2_Game_3_Score'].str.lstrip()
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
df['Team_1'] = df['Team_1'].str[:-1]
df['Team_1_City'] = df['Team_1_City'].str[1:]
df['Team_1_State'] = df['Team_1_State'].str[1:]
df['Team_1_Zip'] = df['Team_1_Zip'].str[1:]
# df = df[df.Team_1_Games_Won >= 0]
# df = df[df.Team_2_Games_Won >= 0]
df = df.drop_duplicates()
# df = df.dropna(subset=['Team_1', 'Team_1_Games_Won', 'Team_2', 'Team_2_Games_Won', 'Result_Team_1', 'Team_1_Home_Away', 'League_District_Nondistrict', 'Date', 'Time', 'Team_2_City', 'Team_2_State', 'Team_1_Street_Address', 'Team_1_City', 'Team_1_State', 'Team_1_Zip'])
df = df.dropna(subset=['Team_1', 'Team_1_Games_Won', 'Team_2', 'Team_2_Games_Won', 'Result_Team_1', 'Team_1_Home_Away', 'League_District_Nondistrict', 'Date', 'Time', 'Team_2_City', 'Team_2_State'])
df.to_csv('clean_windows_volleyball_1.csv')

# notify.send('Finished')


