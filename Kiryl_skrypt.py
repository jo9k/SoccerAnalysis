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
conn = sqlite3.connect(r"C:/Users/ernest.chocholowski/Desktop/Datasets/Soccer/database.sqlite")
cur = conn.cursor()

#Checking if it works fine
cur.execute("select * from country;").fetchall()

#Match Table___________________________________________________________________
#Creating pandas dataframe from table Match
match_df = pd.read_sql_query("select * from match", conn)
match_df.head(10)
match_df.tail(10)
match_df.describe()


#Creating LOTS OF HISTOGRAMS
#match_df.hist(figsize = (100, 100))

#Home, Draw, Away odds for all bookmakers
bookies = ['B365', 'BW', 'IW', 'LB', 'PS', 'WH', 'SJ', 'VC', 'GB', 'BS']
bookies_H = [bookie+'H' for bookie in bookies]
bookies_A = [bookie+'A' for bookie in bookies]
bookies_D = [bookie+'D' for bookie in bookies]

for home, draw, away in zip(bookies_H,bookies_A,bookies_D):
    fig, ax = plt.subplots()
    sns.distplot(match_df[home].dropna(), ax=ax)
    sns.distplot(match_df[draw].dropna(), ax=ax)
    sns.distplot(match_df[away].dropna(), ax=ax)
    #set title
    plt.title(home[:-1], fontsize=16)
    #remove x label
    ax.set_xlabel('')
    ax.set_xlim([0, 8])
    plt.show()

#_______All bookmakers - Home/Draw/Away odds | KDE + BOXPLOTS
bookies_types = {'Home odds':bookies_H, 'Draw odds':bookies_D, 'Away odds':bookies_A}
for bookie_type, bookie_list in bookies_types.items():
    fig, ax = plt.subplots()
    ax.set_xlim([0, 8])
    if bookie_type=='Home odds':
        ax.set_ylim([0, 0.65])
    elif bookie_type =='Draw odds':
        ax.set_ylim([0, 2.3])
    else:
        ax.set_ylim([0, 0.35])
    for bookie in bookie_list:
        sns.distplot(match_df[bookie].dropna(), ax = ax, label=bookie, hist = False)
    #set title
    plt.title('Kernel Density Estimation of '+str(bookie_type)+' by bookie', fontsize=16)
    #remove x label
    ax.set_xlabel('')
    #locate legend 
    plt.legend(loc='best')
    plt.figure(figsize=(30,30))
    plt.show()
    col_sel = bookie_list
    bookie_sel_df = match_df[bookie_list]
    ax = sns.boxplot(data=bookie_sel_df, palette='Set2', showmeans=True)
    if bookie_type=='Home odds':
        ax.set_ylim([1, 5])
    elif bookie_type =='Draw odds':
        ax.set_ylim([1, 10])
    else:
        ax.set_ylim([1, 5.5])
    plt.title(str(bookie_type), fontsize=16)
    plt.show()


#Player attributes table_______________________________________________________
players_df = pd.read_sql_query("select * from player_attributes", conn)
players_df.head(1)

#Histogram of Overall Rating variable
sns.distplot(players_df['overall_rating'].dropna())

#Lots of histogram
players_df.hist(figsize = (100, 100))

#How many goals - Home\Away
temp_data = match_df[['home_team_goal', 'away_team_goal']]
color = ['red', 'lime']
fig, ax = plt.subplots()
ax.set_xlim([0, 10])
ax.set_ylim([0, 9500])
sns.distplot(temp_data.dropna(), ax = ax, kde = False, color = color 
             ).add_legend()
plt.show()

#Contingency table
goals_home_vs_away = pd.crosstab(index = match_df["home_team_goal"],
                                 columns = match_df["away_team_goal"])


def label_win (row):
    if row['home_team_goal'] > row['away_team_goal']:
        return 'WIN'
    if row['home_team_goal'] == row['away_team_goal']:
        return 'DRAW'
    if row['home_team_goal'] < row['away_team_goal']:
        return 'LOSE'
new_df = pd.DataFrame()
new_df['RESULT']=match_df.apply(lambda row: label_win(row), axis=1)
