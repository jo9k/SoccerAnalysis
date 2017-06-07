#READ SQL Database and saved_matches_df before executing the code below

#FREAKING CHEATING NO WAITING SO GOOD
matches_df = pd.DataFrame().from_csv(r'C:/Python/Soccer_draft/saved_matches_df')

#Cursor object to execute SQL commands
cur = con.cursor()

#Pandas dataframe to SQL
matches_df.to_sql("matches_new", con, if_exists="replace")

#Home many seasons was a team present
cur.execute("""select home_team_api_id, count(distinct season)
                                from matches_new
                                group by home_team_api_id
                                order by home_team_api_id limit 5""").fetchall()
#So, not every team was present at all the seasons

#Creates a table to count the number of WINS, DRAWS and LOSES for each team when they play AT HOME
home_teams_game_counts = pd.read_sql_query("""select home_team_api_id,
COUNT(CASE WHEN RESULT = 'WIN' THEN 1 ELSE NULL END) AS WIN_COUNT,
COUNT(CASE WHEN RESULT = 'DRAW' THEN 1 ELSE NULL END) AS DRAW_COUNT,
COUNT(CASE WHEN RESULT = 'LOSE' THEN 1 ELSE NULL END) AS LOSE_COUNT,
season
                                from matches_new
                                group by home_team_api_id, season
                                order by home_team_api_id, season""", con)

#Creates a table to count the number of WINS, DRAWS and LOSES for each team when they play AWAY
away_teams_game_counts = pd.read_sql_query("""select away_team_api_id,
COUNT(CASE WHEN RESULT = 'LOSE' THEN 1 ELSE NULL END) AS WIN_COUNT,
COUNT(CASE WHEN RESULT = 'DRAW' THEN 1 ELSE NULL END) AS DRAW_COUNT,
COUNT(CASE WHEN RESULT = 'WIN' THEN 1 ELSE NULL END) AS LOSE_COUNT,
season
                                from matches_new
                                group by away_team_api_id, season
                                order by away_team_api_id, season""", con)


#New things_______________________________________________________________________________________________________
#Merging two table into one
teams_games_count = pd.DataFrame()
teams_games_count['team_api_id'] = home_teams_game_counts['home_team_api_id']
teams_games_count['WIN_COUNT'] = home_teams_game_counts['WIN_COUNT'] + away_teams_game_counts['WIN_COUNT']
teams_games_count['DRAW_COUNT'] = home_teams_game_counts['DRAW_COUNT'] + away_teams_game_counts['DRAW_COUNT']
teams_games_count['LOSE_COUNT'] = home_teams_game_counts['LOSE_COUNT'] + away_teams_game_counts['LOSE_COUNT']
teams_games_count['season'] = home_teams_game_counts['season']

#Counts all matches
teams_games_count['ALL_COUNT'] = teams_games_count['WIN_COUNT'] + teams_games_count['DRAW_COUNT'] + teams_games_count['LOSE_COUNT']

#Percetange Results
teams_games_count['WIN_percent'] = teams_games_count['WIN_COUNT'] / teams_games_count['ALL_COUNT']
teams_games_count['DRAW_percent'] = teams_games_count['DRAW_COUNT'] / teams_games_count['ALL_COUNT']
teams_games_count['LOSE_percent'] = teams_games_count['LOSE_COUNT'] / teams_games_count['ALL_COUNT']

#Rearrange columns
teams_games_count = teams_games_count[['team_api_id', 'season', 'WIN_COUNT', 'DRAW_COUNT', 'LOSE_COUNT',
       'ALL_COUNT', 'WIN_percent', 'DRAW_percent', 'LOSE_percent']]

#Dummy variables datasets_________________________________________________________________________________________
#Use after reading short_df

#New data set for categorized features
category_short_df = pd.DataFrame()
vars_to_categorize = ['home_player_1_overall_rating', 'away_player_1_overall_rating',
       'home_defenders_score', 'home_midfielders_score',
       'home_forwarders_score', 'away_defenders_score',
       'away_midfielders_score', 'away_forwarders_score']
for category in vars_to_categorize:
    category_short_df[category] = pd.cut(short_df[category], bins = 7, precision = 1)

#Adding the rest of the variables from the original dataset that didn't need categorization
vars_to_add = ['Age_home', 'Age_away', 'Home_odds', 'Draw_odds', 'Away_odds', 'home_formation',
       'away_formation', 'VSPointDiff', 'entropy', 'RESULT']
for add_var in vars_to_add:
    category_short_df[add_var] = short_df[add_var]
    
#Creating Dataframes with Dummy variables: 1 Dataset = All columns for 1 variable
to_dummy = ['home_player_1_overall_rating', 'away_player_1_overall_rating',
       'home_defenders_score', 'home_midfielders_score',
       'home_forwarders_score', 'away_defenders_score',
       'away_midfielders_score', 'away_forwarders_score', 'home_formation',
       'away_formation']
dummy_short_df = {}

for dummy in to_dummy:
    dummy_short_df[dummy] = pd.get_dummies(category_short_df[dummy], prefix = dummy, drop_first = True)
    
#NOT FINISHED YET - TRYING TO MERGE ALL DATASETS INTO 1
dict_names = ['home_player_1_overall_rating', 'away_player_1_overall_rating', 'home_defenders_score', 
              'home_midfielders_score', 'home_forwarders_score', 'away_defenders_score', 'away_midfielders_score', 
              'away_forwarders_score', 'home_formation', 'away_formation']
with_dummy_df = pd.DataFrame()
for df in dict_names:
    with_dummy_df = pd.merge(category_short_df, df, on = df.index.values)