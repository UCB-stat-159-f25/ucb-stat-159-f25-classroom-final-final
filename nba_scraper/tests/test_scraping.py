from nba_scraper.data_scraping import scrape_table, scrape_salaries
import pytest
import requests

def test_scrape_table_returns_dataframe():
    """Test that scrape_table returns a pandas DataFrame for valid inputs"""
    # use actual Basketball Reference URL for 2024-2025 season
    url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
    table_id = "per_game_stats"
    
    result = scrape_table(url, table_id)
    
    # check that we got a DataFrame as its not none
    assert result is not None, "Function should return a DataFrame, not None"
    
    # check that it has expected attributes
    assert hasattr(result, 'shape'), "Result should have 'shape' attribute"
    assert hasattr(result, 'columns'), "Result should have 'columns' attribute"
    assert hasattr(result, 'head'), "Result should have 'head' method"
    
    # check it has some data
    assert result.shape[0] > 0, "DataFrame should have rows"
    assert result.shape[1] > 0, "DataFrame should have columns"
    
    # check header rows were removed
    if 'Rk' in result.columns:
        assert 'Rk' not in result['Rk'].values, "Header rows should be removed"

def test_scrape_table_missing_table():
    """Test missing table returns None"""
    url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
    invalid_table_id = "this_table_does_not_exist"
    
    result = scrape_table(url, invalid_table_id)
    
    # shouldreturn None 
    assert result is None, f"Expected None for missing table, got: {type(result)}"

def test_scrape_salaries_success():
    """Test successful salary scraping"""
    url = "https://www.basketball-reference.com/contracts/players.html"
    
    result = scrape_salaries(url)
    
    if result is None:
        pytest.skip("Network issue")

    # assertions
    assert result is not None
    assert 'Player' in result.columns
    assert 'Rk' in result.columns
    assert result['Rk'].dtype == int

def test_scrape_salaries_basic_functionality():
    """Test that scrape_salaries returns a cleaned DataFrame with salary data"""
    # use actual Basketball Reference salaries URL
    url = "https://www.basketball-reference.com/contracts/players.html"
    table_id = "player-contracts"
    
    result = scrape_salaries(url, table_id)
    
    # skip if network issue or page unavailable
    if result is None:
        pytest.skip("Cannot reach Basketball Reference salaries page")
    
    # should return a DataFrame
    assert result is not None
    assert len(result) > 0, "Should have player rows"
    assert len(result.columns) > 0, "Should have salary columns"
    
    # check DataFrame has expected salary columns
    expected_cols = ['Player', 'Tm', 'Rk']
    for col in expected_cols:
        assert col in result.columns, f"Should have '{col}' column"
    
    # check Rk column is integer
    assert result['Rk'].dtype == int, "Rk column should be integer after cleaning"
    
    # should not have header rows (where first column is 'Rk')
    if 'Rk' in result.columns:
        assert 'Rk' not in result['Rk'].values, "Should remove header rows"

def test_scrape_salaries_error_handling1():
    """Test that scrape_salaries handles errors by returning None"""
    # invalid URL returns None
    with pytest.raises(requests.exceptions.ConnectionError):
        result1 = scrape_salaries("https://invalid-url-that-does-not-exist-12345.com", "player-contracts")
        assert result1 is None, "Invalid URL should return None"
    
def test_scrape_salaries_error_handling2():
    """Test that scrape_salaries handles errors by returning None"""    
    # valid URL but invalid table ID returns None
    result2 = scrape_salaries(
        "https://www.basketball-reference.com/contracts/players.html",
        "invalid-table-id-123"
    )
    assert result2 is None, "Invalid table ID should return None"
    