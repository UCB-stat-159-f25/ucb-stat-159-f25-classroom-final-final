"""
Implementation of functions used throughout final project (divided into helper functions and analysis functions).
"""

### LIBRARIES ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
import random

### HELPER FUNCTIONS ###

## --[[NOTEBOOK 1: Intro Exploration]]-- ##
def summarize_group(df):
    '''
    Given a dataframe, returns a statistical summary in the form of a Series of the data. 
    Serves as an intermediate function to help with group-wise operations.
    '''
    min_idx = df["average_rankings"].idxmin()
    max_idx = df["average_rankings"].idxmax()

    return pd.Series({
        "num_characters": df["character"].nunique(),
        "min_character": df.loc[min_idx, "character"],
        "min_ranking": df.loc[min_idx, "average_rankings"],
        "max_character": df.loc[max_idx, "character"],
        "max_ranking": df.loc[max_idx, "average_rankings"],
        "avg_average_rankings": df["average_rankings"].mean(),
        "std_average_rankings": df["average_rankings"].std()
    })

### ANALYSIS FUNCTIONS ###

## --[[NOTEBOOK 1: Intro Exploration]]-- ##

def initial_data_look(data):
    '''
    An initial exploration of the data with inspection of rows and columns, datatypes, and missing values.
    '''
    print("Here are the first 5 rows of the data:")
    display(data.head())
    print("---------------------------------------------------------")
    print("The number of rows and columns in this dataset are", data.shape)
    print("---------------------------------------------------------")
    print("Here are the data types of each of the columns:")
    display(data.info())
    print("---------------------------------------------------------")
    print("Checking if there are any missing values:", np.mean(data.isna()))

def most_right(data, column_name):
    '''
    Given a dataframe and column_name, retrieves the most right: character, source, [column name] from the data.
    '''
    most_right = data.nlargest(n=10, columns=[column_name])
    most_right = most_right[["character", "source", column_name]]
    print(most_right)

def most_left(data, column_name):
    '''
    Given a dataframe and column_name, retrieves the most left: character, source, and [column name] from the data.
    '''
    most_left = data.nsmallest(n=10, columns=[column_name])
    most_left = most_left[["character", "source", column_name]]
    print(most_left)
        
def explore_bap_averages(data, groups=False):
    '''
    Given a dataframe, utilizes the summarize_group helper function to display statistical summaries in sorted order as well as average_ranking.
    '''
    if not groups:
        overall_min = data["average_rankings"].min()
        overall_max = data["average_rankings"].max()

        return data.loc[
            (data["average_rankings"] == overall_min) |
            (data["average_rankings"] == overall_max),
            ["character", "source", "average_rankings"]
        ]

    return (
        data
        .groupby("source", as_index=False)
        .apply(summarize_group, include_groups=False)
        .sort_values("num_characters", ascending=False)
        .reset_index(drop=True)
    )

def update_correlation(selected_columns, data, all_columns, default_n=10):
    '''
    Given selected columns, dataframe, all columns and n, it is a function to update the heatmap.
    '''
    if not selected_columns:
        return

    subset = data[list(selected_columns)]
    corr = subset.corr().round(2)
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1,
        title="Correlation Matrix of Selected BAPs"
    )
    fig.update_layout(width=700, height=700)
    fig.show()

    if tuple(selected_columns) == tuple(all_columns[:default_n]):
        fig.write_html("visualizations/default_correlation_map.html")
        
def interactive_correlation(char_score_data, col_slice=slice(3, 465), default_n=10):
    '''
    Given the dataframe, columns to slice from and default n creates a widget which is our correlation heatmap.
    '''
    columns = char_score_data.iloc[:, col_slice].columns.tolist()

    column_selector = widgets.SelectMultiple(
        options=columns,
        value=tuple(columns[:default_n]),
        description="Traits",
        disabled=False
    )

    widgets.interact(
        update_correlation,
        selected_columns = column_selector,
        data = widgets.fixed(char_score_data),
        all_columns = widgets.fixed(columns),
        save_default_to = widgets.fixed("visualizations/default_correlation_map.html"),
        default_n = widgets.fixed(default_n),
    )

## --[[NOTEBOOK 3: Identify Archtypes]]-- ##

def llf(xx):
    '''
    Custom leaf label function used in Hierarchical Clustering Dendogram."
    '''
    return "{}".format(temp[xx])