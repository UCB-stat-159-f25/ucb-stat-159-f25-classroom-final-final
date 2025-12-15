from utilities.functions import *
import pytest

data = {
        'severity_index': [1.0, 5.0, 9.0],
        'casualties': [0, 1, 5],
        'economic_loss_usd': [1000, 50000, 100000]
    }

df = pd.DataFrame(data)

def test_plot_bivariate_scatter():
    """
    Checks that plot_bivariate_scatter raises a KeyError if a specified
    x_column does not exist in the DataFrame.
    """
    with pytest.raises(KeyError):
        plot_bivariate_scatter(
            data=df,
            y_column='severity_index',
            x_columns=['casualties', 'non_existent'], 
            n_rows=1,
            n_cols=2,
        )

def test_remove_iqr_outliers():
    """
    Checks that remove_iqr_outliers raises a ValueError if the
    'columns' argument is not a list/array (e.g., if it's a string).
    """
    with pytest.raises(ValueError):
        remove_iqr_outliers(df, columns="severity_index") 

def test_transform_features():
    """
    Checks that transform_features raises a TypeError if the input 'df'
    is not a pandas DataFrame.
    """
    bad_input = [1, 2, 3]
    with pytest.raises(TypeError):
        transform_features(bad_input)




