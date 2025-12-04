import os
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings 

def scrape_table(url: str, table_id: str):
    """
    Scrape a specific HTML table from a webpage and convert it to a pandas DataFrame.
    
    This function searches for a table by its HTML id attribute, first looking within
    HTML comments (where Basketball Reference often embeds tables) and then in the 
    main document body. The resulting DataFrame is cleaned by removing header rows
    that repeat column names.
    
    Parameters
    ----------
    url : str
        The URL of the webpage containing the table to scrape.
    table_id : str
        The HTML id attribute of the target table (e.g., 'per_game_stats').
        
    Returns
    -------
    pd.DataFrame or None
        A pandas DataFrame containing the scraped table data, cleaned of header rows.
        Returns None if the request fails or the table is not found.
    """
    # setting up headers to mimic a browser request
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if not response.ok:
        print(f"Failed to fetch URL: {url}")
        return None

    # parsing HTML content of the response
    soup = BeautifulSoup(response.content, 'lxml')

    table = None
    # searching for table using the specified table_id
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and table_id in text):
        comment_soup = BeautifulSoup(comment, 'lxml')
        # find the table by id
        table = comment_soup.find('table', {'id': table_id})  
        if table:
            break

    # if no table is found in comments, search directly in the body of the page
    if not table:
        table = soup.find('table', {'id': table_id})

    if not table:
        print(f"Table '{table_id}' not found")
        return None
        
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FutureWarning)
        # converting HTML table into pandas data frame
        df = pd.read_html(StringIO(str(table)))[0]
        # removing rows where the 'Rk' column has the value 'Rk'
        df = df[df['Rk'] != 'Rk']
        # resetting the data frame index to clean up
        df.reset_index(drop=True, inplace=True)
        return df

def scrape_and_merge_stats(season: int, save_dir: str = 'nba_merged_stats'):
    """
    Scrape both per-game and advanced statistics for a given NBA season and merge them.
    
    This function scrapes the per-game statistics table and advanced statistics table
    from Basketball Reference for the specified season, merges them on common player
    identifiers, adds a season column, and saves the result as a CSV file.
    
    Parameters
    ----------
    season : int
        The ending year of the NBA season.
    save_dir : str, default='nba_merged_stats'
        Directory where the merged CSV file will be saved.
        
    Returns
    -------
    None
        The function saves a CSV file to disk but does not return a value directly.
        Prints status messages about the scraping and saving process.
    """
    # create the directory if doesn't exist
    os.makedirs(save_dir, exist_ok=True)  

    # URLs for per-game and advanced statistics
    per_game_url = f'https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html'
    advanced_url = f'https://www.basketball-reference.com/leagues/NBA_{season}_advanced.html'

    # scraping the two tables given URLs
    per_game_df = scrape_table(per_game_url, 'per_game_stats')
    advanced_df = scrape_table(advanced_url, 'advanced')

    # checking if any of the tables failed to scrape data
    if per_game_df is None or advanced_df is None:
        print(f"Skipping season {season} due to missing data.")
        return

    # merging the per-game and advanced stats on common columns
    merged_df = pd.merge(per_game_df, advanced_df, on=['Player', 'Team', 'Age', 'Pos', 'G', 'GS', 'Awards'], how='inner')
    # dropping unnecessary columns from the merged data frame
    merged_df = merged_df.drop(columns=["Rk_y", "MP_y"])
    # adding the season column in the format "2024-25" for the given year
    merged_df['Season'] = f'{season-1}-{str(season)[-2:]}'

    # saving the merged data frame as a CSV file
    merged_df.to_csv(f"{save_dir}/nba_merged_{season}.csv", index=False)
    print(f"Merged stats saved for {season}: nba_merged_{season}.csv")

def scrape_salaries(url: str, table_id: str = "player-contracts"):
    """
    Scrape NBA player salary data from a webpage and clean the resulting DataFrame.
    
    This function extracts salary information from an HTML table, handling both 
    tables embedded in HTML comments (common on Basketball Reference) and those
    in the main document body. It performs cleaning operations including header
    row removal, MultiIndex column flattening, and numeric conversion of rank data.
    
    Parameters
    ----------
    url : str
        The URL of the webpage containing the salary table to scrape.
    table_id : str
        The HTML id attribute of the target salary table (e.g., 'salaries').
        
    Returns
    -------
    pd.DataFrame or None
        A cleaned pandas DataFrame containing salary data with:
        - Rk (rank) column converted to integers
        - Header rows removed
        - MultiIndex columns flattened
        Returns None if the request fails or the table is not found.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if not response.ok:
        print(f"Failed to fetch URL: {url}")
        return None
    
    # parse HTML content
    soup = BeautifulSoup(response.content, 'lxml') 

    table = None
    # searching for the table in the HTML comments by table_id
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and table_id in text):
        comment_soup = BeautifulSoup(comment, 'lxml')
        table = comment_soup.find('table', {'id': table_id})
        if table:
            break

    # if no table is found in comments, search directly in the body of the page
    if not table:
        table = soup.find('table', {'id': table_id})

    if not table:
        print(f"Table '{table_id}' not found")
        return None
        
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FutureWarning)
        # reading table into a data frame
        df = pd.read_html(StringIO(str(table)), skiprows=0)[0]
        # filtering rows where the 'Rk' column has the value 'Rk' (header rows)
        df = df[(df.iloc[:, 0] != 'Rk') & (df.iloc[:, 0].notna())]
        # dropping the level 0 column if it's a MultiIndex object
        df.columns = df.columns.droplevel(0) if isinstance(df.columns, pd.MultiIndex) else df.columns
        df.reset_index(drop=True, inplace=True)
        
        # converting 'Rk' to numeric and removing rows with NaN in 'Rk'
        df['Rk'] = pd.to_numeric(df['Rk'], errors='coerce')
        df.dropna(subset=['Rk'], inplace=True)
        df['Rk'] = df['Rk'].astype(int)

        return df
