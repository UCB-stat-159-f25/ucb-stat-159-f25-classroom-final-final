from finaltools.finaltools import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
import random
from sklearn.preprocessing import StandardScaler

# First Test - sanity test for summarize_group
def test_summarize_group():
    df = pd.DataFrame({
        "character": ["A", "A", "B", "C", "C"],
        "average_rankings": [0.2, 0.4, 0.1, 0.9, 0.8],
        "source": ["s1", "s1", "s1", "s2", "s2"],
    })

    res = summarize_group(df)
    assert isinstance(res, pd.Series)

# Second Test - accuracy test for summarize_group
def test_summarize_group_2():
    df = pd.DataFrame({
        "character": ["A", "B", "C", "B"],
        "average_rankings": [1.0, 2.0, 4.0, 3.0],
        "source": ["x", "x", "x", "x"],
    })

    res = summarize_group(df)

    assert res["num_characters"] == 3
    assert res["min_character"] == "A"
    assert res["min_ranking"] == 1.0
    assert res["max_character"] == "C"
    assert res["max_ranking"] == 4.0

    expected_mean = df["average_rankings"].mean()
    expected_sd = df["average_rankings"].std(ddof=1)
    assert res["avg_average_rankings"] == expected_mean
    assert np.isclose(res["std_average_rankings"], expected_sd)

# Third Test - sanity test for initial_data_look
def test_initial_data_look():
    df = pd.DataFrame({
        "A": ["alpha", "beta", "gamma"]
    })

    initial_data_look(df)
    assert isinstance(df, pd.DataFrame)