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

#NOT FINISHED - NEED HELP
#Function that calculates the overall rating separatly for defenders, midfielders and forwarders
def calculate_group_ratings (row, home_flag):
    
#Define the vectors needed    
    home_player_positions = ['home_player_2_position',
       'home_player_3_position', 'home_player_4_position',
       'home_player_5_position', 'home_player_6_position',
       'home_player_7_position', 'home_player_8_position',
       'home_player_9_position', 'home_player_10_position',
       'home_player_11_position']
    away_player_positions = ['away_player_2_position', 'away_player_3_position',
       'away_player_4_position', 'away_player_5_position',
       'away_player_6_position', 'away_player_7_position',
       'away_player_8_position', 'away_player_9_position',
       'away_player_10_position', 'away_player_11_position']
    
    defenders = ['SW', 'RB', 'CB', 'LB', 'RWB', 'LWB']
    midfielders = ['DM', 'CM', 'LW', 'RW', 'AM']
    forwarders = ['RWF', 'CF', 'LWF']
    
    home_player_ratings = ['home_player_2_overall_rating',
       'home_player_3_overall_rating', 'home_player_4_overall_rating',
       'home_player_5_overall_rating', 'home_player_6_overall_rating',
       'home_player_7_overall_rating', 'home_player_8_overall_rating',
       'home_player_9_overall_rating', 'home_player_10_overall_rating',
       'home_player_11_overall_rating']
    away_player_ratings = ['away_player_2_overall_rating', 'away_player_3_overall_rating',
       'away_player_4_overall_rating', 'away_player_5_overall_rating',
       'away_player_6_overall_rating', 'away_player_7_overall_rating',
       'away_player_8_overall_rating', 'away_player_9_overall_rating']

#[0] - defenders, [1] - midfielders, [2] - forwarders
    home_counts = [0, 0, 0]
    away_counts = [0, 0, 0]
    home_defenders_vector = []
    home_midfielders_vector = []
    home_forwarders_vector = []
    away_defenders_vector = []
    away_midfielders_vector = []
    away_forwarders_vector = []
    home_sums = []
    away_sums = []
    home_ratings = []
    away_ratings = []

#Counts the number of players in Defenders, Midfielders, Forwarders    
    for home_pos, away_pos, in zip(home_player_positions, away_player_positions):
        home = row[home_pos]
        away = row[away_pos]
        if home in defenders:
            home_counts[0] += 1
        elif home in midfielders:
            home_counts[1] += 1
        else:
            home_counts[2] += 1
            
        if away in defenders:
            away_counts[0] += 1
        elif away in midfielders:
            away_counts[1] += 1
        else:
            away_counts[2] += 1

#HOME - Creates vector containg overall rating values separately for Defenders, Midfielders, Forwarders            
    for player_nr in range(2, 12):
        player_pos = row['home_player_' + player_nr + '_position']
        player_rtng = row['home_player_' + player + '_overall_rating']
        if player_pos in defenders:
            home_defenders_vector.append(player_rtng[0])
        elif player_pos in midfielders:
            home_midfielders_vector.append(player_rtng[0])
        else:
            home_forwarders_vector.append(player_rtng[0])
    
#AWAY - Creates vector containg overall rating values separately for Defenders, Midfielders, Forwarders            
    for player_nr in range(2, 12):
        player_pos = row['away_player_' + player_nr + '_position']
        player_rtng = row['away_player_' + player + '_overall_rating']
        if player_pos in defenders:
            away_defenders_vector.append(player_rtng[0])
        elif player_pos in midfielders:
            away_midfielders_vector.append(player_rtng[0])
        else:
            away_forwarders_vector.append(player_rtng[0])
            
#Calculating sums
    home_sums.append(home_defenders_vector.sum())
    home_sums.append(home_midfielders_vector.sum())
    home_sums.append(home_forwarders_vector.sum())
    away_sums.append(away_defenders_vector.sum())
    away_sums.append(away_midfielders_vector.sum())
    away_sums.append(away_forwarders_vector.sum())

#Counts the average of overall rating in Defeders, Midfieldes and Forwarders
    home_ratings.append(home_sums[0]/home_counts[0])
    home_ratings.append(home_sums[1]/home_counts[1])
    home_ratings.append(home_sums[2]/home_counts[2])
    away_ratings.append(home_sums[0]/home_counts[0])
    away_ratings.append(home_sums[1]/home_counts[1])
    away_ratings.append(home_sums[2]/home_counts[2])
    
    if home_flag == True:
        return home_ratings
    else:
        return away_ratings