#Soccer Dataset Analysis_______________________________________________________

#Import libraries
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.precision', 3)
pd.set_option('display.max_columns', 115)
pd.set_option('display.width', 160)
#Etablishing connection with SQL database and creating cursor object
conn = sqlite3.connect(r"C:/Python/Soccer1/database.sqlite")
cur = conn.cursor()

#Checking if it works fine
cur.execute("select * from country;").fetchall()

#Match Table___________________________________________________________________
#Creating pandas dataframe from table Match
full_df = pd.read_sql_query("select * from match", conn)
full_df.head(10)
full_df.tail(10)
full_df.describe()


#Creating LOTS OF HISTOGRAMS
full_df.hist(figsize = (100, 100))

#B365 Home, Draw, Away odds
full_df['B365H'].isnull().sum()
sns.distplot(full_df['B365H'].dropna())
sns.distplot(full_df['B365A'].dropna())
sns.distplot(full_df['B365D'].dropna())

fig, ax = plt.subplots()
ax.set_xlim([0, 15])
ax.set_ylim([0, 1.4])
sns.distplot(full_df['B365H'].dropna(), ax = ax)
sns.distplot(full_df['B365A'].dropna(), ax = ax)
sns.distplot(full_df['B365D'].dropna(), ax = ax)
plt.show()

#Home, Draw, Away odds for all bookmakers
bookmaker_names = ['B365', 'BW', 'IW' ,'LB', 'PS', 'WH', 'SJ', 'VC' ,'GB', 'BS']
odds_types = ['H', 'D', 'A']
bookmaker_dict = {}

for name in bookmaker_names:
    bookmaker_dict[name]=[]
    for odd_type in odds_types:
        bookmaker_dict[name].append(odd_type)
        
for name,odd_type in bookmaker_dict.items():
    for i in range (3):
        colname = str(name)+str(odd_type[i])
        sns.distplot(full_df[colname].dropna(), ax=ax)
    plt.show()
    

#All bookmakers - Home odds
fig, ax = plt.subplots()
ax.set_xlim([0, 8])
ax.set_ylim([0, 0.7])
for name,odd_type in bookmaker_dict.items():
    colname = str(name)+str(odd_type[0])
    sns.distplot(full_df[colname].dropna(), ax = ax, hist = False)
plt.show()

#All bookmakers - Draw odds
fig, ax = plt.subplots()
ax.set_xlim([0, 8])
ax.set_ylim([0, 2.5])
for name,odd_type in bookmaker_dict.items():
    colname = str(name)+str(odd_type[1])
    sns.distplot(full_df[colname].dropna(), ax = ax, hist = False)
plt.show()

#All bookmakers - Away odds
fig, ax = plt.subplots()
ax.set_xlim([0, 8])
ax.set_ylim([0, 0.35])
for name,odd_type in bookmaker_dict.items():
    colname = str(name)+str(odd_type[2])
    sns.distplot(full_df[colname].dropna(), ax = ax, hist = False)
plt.show()

#Player attributes table_______________________________________________________
full_players = pd.read_sql_query("select * from player_attributes", conn)
full_players.head(1)

#Histogram of Overall Rating variable
sns.distplot(full_players['overall_rating'].dropna())

#Lots of histogram
full_players.hist(figsize = (100, 100))

#How many goals - Home\Away
temp_data = full_df[['home_team_goal', 'away_team_goal']]
color = ['red', 'lime']
fig, ax = plt.subplots()
ax.set_xlim([0, 10])
ax.set_ylim([0, 9500])
sns.distplot(temp_data.dropna(), ax = ax, kde = False, color = color 
             ).add_legend()
plt.show()

#Contingency table
goals_home_vs_away = pd.crosstab(index = full_df["home_team_goal"],
                                 columns = full_df["away_team_goal"])

goals_home_vs_away

