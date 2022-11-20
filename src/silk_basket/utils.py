import numpy as np
import pandas as pd

def calc_ma(df, window, column=None):

    if not column:
        df = df.rolling(window=window).mean()
    else:
        df = df.rolling(window=window)[column].mean()

    return df

def calc_price_change():
    pass

def calc_perc_row(df):
    if not 'Total' in df.columns:
        df['Total'] = df.sum(axis=1)

    df = df.replace(np.nan, 0)

    perc_df = df.div(df['Total'],axis=0) * 100

    return perc_df

def transfer_date_to_datetime(df, column, format=None, set_index=True):
    """
    format example: '%YYYY%mm%dd'
    """
    datetime_col = pd.to_datetime(df[column], format=format)
    df.loc[:, column] = datetime_col
    if set_index:
        df.set_index(column, inplace=True)

    return df