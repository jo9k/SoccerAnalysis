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