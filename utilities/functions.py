import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_bivariate_scatter(
    data,
    y_column,
    x_columns=None,
    sample_size=5000,
    n_rows=2,
    n_cols=3,
):
    """
    Creates bivariate scatter plots with a common dependent variable.

    Parameters
    ----------
    data : pandas.DataFrame
        Input dataset.
    y_column : str
        Dependent variable (y-axis).
    x_columns : list of str, optional
        Independent variables. If None, all columns except y_column are used.
    sample_size : int, optional
        Number of rows to sample.
    random_state : int, optional
        Random seed for reproducibility.
    n_rows : int, optional
        Number of subplot rows.
    n_cols : int, optional
        Number of subplot columns.
    figsize : tuple, optional
        Figure size.
    color : str, optional
        Scatter plot color.
    alpha : float, optional
        Point transparency.
    point_size : int, optional
        Marker size.
    """

    # Sample data
    sampled_data = data.sample(
        n=min(sample_size, len(data)),
        random_state=42,
        replace=False
    )

    # Determine x columns
    if x_columns is None:
        x_columns = [col for col in sampled_data.columns if col != y_column]

    subset = sampled_data[x_columns + [y_column]]

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 10))
    axes = axes.flatten()

    for i, col in enumerate(x_columns):
        ax = axes[i]
        ax.scatter(
            subset[col],
            subset[y_column],
            color='darkgreen'
        )
        ax.set_title(
            f'Sampled Data ({len(subset)} pts): {col} vs. {y_column}',
            fontsize=14
        )
        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel(y_column, fontsize=12)
        ax.grid(True, linestyle=':', alpha=0.5)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle(
        f'Bivariate Scatter Plots with {y_column} as Dependent Variable '
        f'(Sample of {len(subset)} Rows)',
        fontsize=18,
        y=1.02
    )

    plt.tight_layout()
    plt.show()

def remove_iqr_outliers(df, columns, k=1.5):
    """
    Removes rows that contain outliers in any of the specified columns
    using the k * IQR rule.
    """
    mask = pd.Series(True, index=df.index)

    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - k * iqr
        upper = q3 + k * iqr

        mask &= df[col].between(lower, upper)

    return df[mask]


def transform_features(df):
	df['severity_index'] = df['severity_index']  # no transform

	df['casualties'] = np.log1p(df['casualties'])
	
	df['economic_loss_usd'] = np.log1p(df['economic_loss_usd'])
	
	df['response_time_hours'] = np.log1p(df['response_time_hours'])
	
	df['aid_amount_usd'] = np.log1p(df['aid_amount_usd'])
	
	df['response_efficiency_score'] = np.log1p(
	    100 - df['response_efficiency_score'])
	outlier_columns = [
    'severity_index',
    'casualties',
    'economic_loss_usd',
    'response_time_hours',
    'aid_amount_usd',
    'response_efficiency_score'
	]
	processed_df = remove_iqr_outliers(
    df,
    columns=outlier_columns,
    k=1.5)
	return processed_df

	
