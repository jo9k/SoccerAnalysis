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
    for odds in [home, draw, away]:
        sns.distplot(match_df[odds].dropna(), ax=ax, label=odds, hist = False)
    #set title
    plt.title(home[:-1], fontsize=16)
    #remove x label
    ax.set_xlabel('')
    ax.set_xlim([0, 8])
    plt.show()

#_______All bookmakers - Home/Draw/Away odds | KDE + BOXPLOTS
bookies_types = {'Home odds':bookies_H, 'Draw odds':bookies_D, 'Away odds':bookies_A}
for bookie_type, bookie_list in bookies_types.items():
    fig, axes = plt.subplots(ncols=2)
    axes[0].set_xlim([0, 8])
    if bookie_type=='Home odds':
        axes[0].set_ylim([0, 0.65])
    elif bookie_type =='Draw odds':
        axes[0].set_ylim([0, 2.3])
    else:
        axes[0].set_ylim([0, 0.35])
    for bookie in bookie_list:
        sns.distplot(match_df[bookie].dropna(), ax = axes[0], label=bookie, hist = False)
    #set title
    #remove x label
    axes[0].set_xlabel('')
    #locate legend 
    plt.legend(loc='best')
    col_sel = bookie_list
    bookie_sel_df = match_df[bookie_list]
    axes[1] = sns.boxplot(data=bookie_sel_df, palette='Set2', showmeans=True)
    if bookie_type=='Home odds':
        axes[1].set_ylim([1, 5])
    elif bookie_type =='Draw odds':
        axes[1].set_ylim([1, 10])
    else:
        axes[1].set_ylim([1, 5.5])
    plt.suptitle(str(bookie_type), fontsize=16)
    plt.figure(figsize=(60,30))
    plt.show()


#Player attributes table_______________________________________________________
players_df = pd.read_sql_query("select * from player_attributes", conn)
players_df.head(1)

#Histogram of Overall Rating variable
sns.distplot(players_df['overall_rating'].dropna())

#Lots of histogram
#players_df.hist(figsize = (100, 100))

#How many goals - Home\Away
goals_df = match_df[['home_team_goal', 'away_team_goal']]
color = ['red', 'lime']
fig, ax = plt.subplots()
ax.set_xlim([0, 10])
ax.set_ylim([0, 9500])
sns.distplot(goals_df.dropna(), ax = ax, kde = False, color = color 
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

match_df['RESULT']=match_df.apply(lambda row: label_win(row), axis=1)



#Split data for train and test
def split_data(data, targ):
    #set target for training
    target = data[targ]

    # Import the train_test_split method
    from sklearn.model_selection import train_test_split
    # Split data into train (3/4th of data) and test (1/4th of data)
    return train_test_split(data.drop('RESULT', axis=1), target, train_size = 0.75, random_state=0);

train, test, target_train, target_test = split_data(match_df, 'RESULT')
data = (train, test, target_train, target_test)

##########################
#######CHANGES BELOW######
#######IRRELEVANT TO######
#######SCRIPT ABOVE#######
#####ONLY FOR NOTEBOOK####
#===========Kiryl_02.06.2017=========================
matches_df['home_team_mean_Age'] = matches_df[['home_player_1_Age',
       'home_player_2_Age', 'home_player_3_Age', 'home_player_4_Age',
       'home_player_5_Age', 'home_player_6_Age', 'home_player_7_Age',
       'home_player_8_Age', 'home_player_9_Age', 'home_player_10_Age',
       'home_player_11_Age']].mean(axis=1)

matches_df['away_team_mean_Age'] = matches_df[['away_player_1_Age', 'away_player_2_Age',
       'away_player_3_Age', 'away_player_4_Age', 'away_player_5_Age',
       'away_player_6_Age', 'away_player_7_Age', 'away_player_8_Age',
       'away_player_9_Age', 'away_player_10_Age', 'away_player_11_Age']].mean(axis = 1)

#Home team mean age minus Away team mean age
matches_df['age_Difference'] = matches_df['home_team_mean_Age'] - matches_df['away_team_mean_Age']

#NOT FINISHED - NEED HELP /// Should be ok now - @E.Ch.
#Function that calculates the overall rating separatly for defenders, midfielders and forwarders
def calculate_group_ratings (row, home_flag, role):
    import numpy as np
    
    #Define the vectors needed    
    if home_flag == True:
        prefix = 'home'
    else:
        prefix = 'away'
    
    players_lst = ['_player_2_', '_player_3_',
       '_player_4_', '_player_5_',
       '_player_6_', '_player_7_',
       '_player_8_', '_player_9_',
       '_player_10_', '_player_11_']
    player_positions = [prefix+player+'position' for player in players_lst]
    player_ratings = [prefix+player+'overall_rating' for player in players_lst]
    
    if role == 'defenders':
        role_list = ['SW', 'RB', 'CB', 'LB', 'RWB', 'LWB']
    elif role == 'midfielders':
        role_list = ['DM', 'CM', 'LW', 'RW', 'AM']
    elif role == 'forwarders':
        role_list = ['RWF', 'CF', 'LWF']

    scores_vector = []

#Counts the number of players in Defenders, Midfielders, Forwarders    
    for position, rank in zip(player_positions, player_ratings):
        pos = row[position]
        if pos in role_list:
            rtng = row[rank]
            scores_vector.append(rtng)

#Counts the average of overall rating in Defeders/Midfieldes/Forwarders    
    return np.mean(scores_vector)

#===========PCA_Kiryl_02.06.2017=====================
#Use this code after scaling the features
#====================================================
from sklearn.decomposition import PCA

pca = PCA(n_components = 2)
pca.fit(scaled_features_df.drop('RESULT', axis = 1))
pca_features_df = pca.transform(scaled_features_df.drop('RESULT', axis = 1))
scaled_features_df.shape
pca_features_df.shape
pca_features_pddf = pd.DataFrame(pca_features_df, index = ml_matches_df.index)
pca_features_pddf.head(1)
pca_features_pddf['RESULT'] = ml_matches_df['RESULT']