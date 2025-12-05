import pandas as pd
import numpy as np
import re

# function to process player contracts
def player_contracts(filepath):
    
    df = pd.read_csv(filepath)
    # fill any missing values with 0.0 (assuming missing salary data)
    df = df.fillna(0.0)
    
    # iterate over specific columns (columns 3 to 10) that hold salary data
    for col in df.iloc[:, 3:10].columns:
        # remove dollar signs and commas, and convert to integer
        df[col] = df[col].replace("[\$,]", '', regex=True).astype(int)

    # get the column names for the current and next season
    current_season = df.iloc[:, 3:10].columns[0]
    next_season = df.iloc[:, 3:10].columns[1]

    # create a new column for contract year indicator
    indicator_col = f"{current_season}_contract_year"

    # contract year indicator: set to 1 if salary > 0 in current season, 0 in next season
    df[indicator_col] = (df[current_season].astype(float) > 0) & (df[next_season].astype(float) == 0)
    
    # convert the indicator column to integer type
    df[indicator_col] = df[indicator_col].astype(int)
    return df

# function to check if a player has won any major awards
def check_award_winner(x):
    awards = ["MVP-1", "DPOY-1", "MIP-1", "CPOY-1", "ROY-1", "6MOY-1"]
    # return 1 if the player has any of the specified awards
    for a in awards:
        if a in x.split(','):
            return 1
    return 0

# functions to check for specific all-NBA or all-defensive team appearances
def all_nba_team_1(x):
    award = 'NBA1'
    if award in x.split(','):
        return 1
    return 0

def all_nba_team_2(x):
    award = 'NBA2'
    if award in x.split(','):
        return 1
    return 0

def all_nba_team_3(x):
    award = 'NBA3'
    if award in x.split(','):
        return 1
    return 0

def all_defensive_1(x):
    award = 'DEF1'
    if award in x.split(','):
        return 1
    return 0

def all_defensive_2(x):
    award = 'DEF2'
    if award in x.split(','):
        return 1
    return 0

# function to check if the team name indicates multiple teams (for free agents)
def is_multi_team(team):
    return bool(re.match(r'\d+TM', str(team)))

# function to fix team labels for players who played for multiple teams
def fix_team_labels(df):
    cleaned_rows = []
    
    # group by player and season
    grouped = df.groupby(['Player'])
    
    for (player), group in grouped:
        # handle players who have 'TM' in their team name (free agents or multiple teams)
        multi_team_row = group[group['Team'].apply(is_multi_team)]
        if not multi_team_row.empty:
            other_teams = group[~group['Team'].apply(is_multi_team)]
            if not other_teams.empty:
                last_team = other_teams.iloc[-1]['Team']
            else:
                last_team = None
            
            row = multi_team_row.iloc[0].copy()
            row['Team'] = last_team
            cleaned_rows.append(row)
        else:
            cleaned_rows.append(group.iloc[0])
    
    return pd.DataFrame(cleaned_rows)
    