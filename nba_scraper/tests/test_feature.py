from nba_scraper.feature_engineering import *

def test_check_award_winner_simple():
    """Simple test for award winner checking."""
    assert check_award_winner("MVP-1") == 1
    assert check_award_winner("All-Star") == 0
    assert check_award_winner("ROY-1,MVP-2") == 1

def test_all_nba_teams_simple():
    """Simple test for All-NBA teams."""
    assert all_nba_team_1("NBA1") == 1
    assert all_nba_team_1("NBA2") == 0
    assert all_nba_team_2("NBA2") == 1
    assert all_nba_team_3("NBA3") == 1

def test_is_multi_team_simple():
    """Simple test for multi-team detection."""
    assert is_multi_team("2TM") == True
    assert is_multi_team("LAL") == False
    assert is_multi_team("3TM") == True

def test_fix_team_labels_simple():
    """Simple test for fixing team labels."""
    import pandas as pd
    
    data = {
        'Player': ['Test Player', 'Test Player'],
        'Team': ['GSW', '2TM']
    }
    df = pd.DataFrame(data)
    
    result = fix_team_labels(df)
    
    # Should have 1 row with corrected team
    assert len(result) == 1
    assert result['Team'].iloc[0] == 'GSW'

def test_check_award_winner_edge_cases():
    """Test award winner function with edge cases."""
    # Empty string
    assert check_award_winner("") == 0
    
    # Only commas
    assert check_award_winner(",") == 0
    
    # Multiple major awards
    assert check_award_winner("MVP-1,DPOY-1,ROY-1") == 1
    
    # Award with extra spaces
    assert check_award_winner("MVP-1 , All-Star") == 0
    
    # Similar but different award (MVP-2 not MVP-1)
    assert check_award_winner("MVP-2,DPOY-2") == 0

def test_all_defensive_teams_comprehensive():
    """Test All-Defensive team functions thoroughly."""
    # First team
    assert all_defensive_1("DEF1") == 1
    assert all_defensive_1("DEF1,All-Star") == 1
    assert all_defensive_1("DEF2,All-Star") == 0
    
    # Second team  
    assert all_defensive_2("DEF2") == 1
    assert all_defensive_2("DEF2,All-Star") == 1
    assert all_defensive_2("DEF1,All-Star") == 0
    
    # Neither team
    assert all_defensive_1("All-Star") == 0
    assert all_defensive_2("") == 0

def test_is_multi_team_variations():
    """Test different variations of multi-team patterns."""
    # Valid patterns
    assert is_multi_team("1TM") == True
    assert is_multi_team("2TM") == True
    assert is_multi_team("9TM") == True
    
    # Invalid patterns
    assert is_multi_team("TM") == False  # No number
    assert is_multi_team("2T") == False  # Missing M
    assert is_multi_team("T2M") == False  # Wrong order
    assert is_multi_team(" 2TM ") == False  # With spaces
    
    # Team abbreviations (should be False)
    assert is_multi_team("LAL") == False
    assert is_multi_team("GSW") == False
    assert is_multi_team("BOS") == False

def test_fix_team_labels_edge_cases():
    """Test team label fixing with edge cases."""
    import pandas as pd
    
    # Player with only TM designation (no other team)
    data1 = {
        'Player': ['Lonely Player'],
        'Team': ['2TM']
    }
    df1 = pd.DataFrame(data1)
    result1 = fix_team_labels(df1)
    assert len(result1) == 1
    assert pd.isna(result1['Team'].iloc[0]) or result1['Team'].iloc[0] is None
    
    # Player with TM first, then actual team
    data2 = {
        'Player': ['Player X', 'Player X'],
        'Team': ['2TM', 'MIA']
    }
    df2 = pd.DataFrame(data2)
    result2 = fix_team_labels(df2)
    assert result2['Team'].iloc[0] == 'MIA'  # Should use last actual team
    
    # Multiple players mixed
    data3 = {
        'Player': ['A', 'A', 'B', 'B', 'C'],
        'Team': ['LAL', '2TM', 'GSW', '3TM', 'BOS']
    }
    df3 = pd.DataFrame(data3)
    result3 = fix_team_labels(df3)
    
    # Should have 3 rows (one per player)
    assert len(result3) == 3
    
    # Player A: TM replaced with last team
    assert result3[result3['Player'] == 'A']['Team'].iloc[0] == 'LAL'
    
    # Player B: TM with no other team = None
    assert result3[result3['Player'] == 'B']['Team'].iloc[0] == 'GSW'
    
    # Player C: No TM, no change
    assert result3[result3['Player'] == 'C']['Team'].iloc[0] == 'BOS'