import pandas as pd
import numpy as np
import re

def player_contracts(filepath: str):
    """
    Load and clean NBA player contract data from a CSV file.
    
    Processes salary columns by removing currency formatting and creates a contract year
    indicator based on salary patterns between current and next season.
    
    Parameters
    ----------
    filepath : str
        Path to the CSV file containing NBA player contract data.
        
    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with:
        - Salary columns converted to integers (currency symbols removed)
        - Missing values filled with 0.0
        - Added contract year indicator column
    """

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

def check_award_winner(x):
    """
    Check if a player has won any major NBA awards.
    
    Examines a comma-separated awards string and returns 1 if any of the 
    specified major awards are present, otherwise returns 0.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards earned by a player.
        Example: "All-Star,ROY-1,MVP-2"
        
    Returns
    -------
    int
        1 if the player has won any major award (MVP-1, DPOY-1, MIP-1, 
        CPOY-1, ROY-1, or 6MOY-1), otherwise 0.
    """
    awards = ["MVP-1", "DPOY-1", "MIP-1", "CPOY-1", "ROY-1", "6MOY-1"]
    # return 1 if the player has any of the specified awards
    for a in awards:
        if a in x.split(','):
            return 1
    return 0

def all_nba_team_1(x):
    """
    Check if a player was selected to All-NBA First Team.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards and honors.
        
    Returns
    -------
    int
        1 if 'NBA1' is in the awards string, otherwise 0.
    """
    award = 'NBA1'
    if award in x.split(','):
        return 1
    return 0

def all_nba_team_2(x):
    """
    Check if a player was selected to All-NBA Second Team.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards and honors.
        
    Returns
    -------
    int
        1 if 'NBA2' is in the awards string, otherwise 0.
    """
    award = 'NBA2'
    if award in x.split(','):
        return 1
    return 0

def all_nba_team_3(x):
    """
    Check if a player was selected to All-NBA Third Team.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards and honors.
        
    Returns
    -------
    int
        1 if 'NBA3' is in the awards string, otherwise 0.
    """
    award = 'NBA3'
    if award in x.split(','):
        return 1
    return 0

def all_defensive_1(x):
    """
    Check if a player was selected to All-Defensive First Team.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards and honors.
        
    Returns
    -------
    int
        1 if 'DEF1' is in the awards string, otherwise 0.
    """
    award = 'DEF1'
    if award in x.split(','):
        return 1
    return 0

def all_defensive_2(x):
    """
    Check if a player was selected to All-Defensive Second Team.
    
    Parameters
    ----------
    x : str
        Comma-separated string of awards and honors.
        
    Returns
    -------
    int
        1 if 'DEF2' is in the awards string, otherwise 0.
    """
    award = 'DEF2'
    if award in x.split(','):
        return 1
    return 0

def is_multi_team(team):
    """
    Check if a team name indicates the player played for multiple teams.
    
    Identifies free agents or players who played for multiple teams in a season
    by checking for the pattern 'XTM' where X is a number (e.g., '2TM', '3TM').
    
    Parameters
    ----------
    team : str
        Team name string to check.
        
    Returns
    -------
    bool
        True if the team name matches the multiple team pattern, False otherwise.
    """
    return bool(re.match(r'\d+TM', str(team)))

def fix_team_labels(df):
    """
    Clean team labels for players who played for multiple teams in a season.
    
    For players with 'TM' team designations (e.g., '2TM'), replaces the designation
    with their last actual team. Groups by player to handle the cleaning.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing player statistics with 'Player' and 'Team' columns.
        
    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with corrected team labels for multi-team players.
        Contains one row per player with accurate team assignment.
    """
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
    