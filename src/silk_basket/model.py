
# Silk basket design
#
# - check assets live on band oracle
# - retrieve price data via outside Api or downloaded dataset.
# - retrieve import/export data per country
# - retrieve gdp data in USD per country
#
# Set up a init_basket method
# - people can make a basket based on gdp, export and price methos and do a custom allocation.
# - this should prompt a 2nd data input where they can parameterize the separate methods.
# . Need time to train on
# . Weighting between poaitive and negative currencies for the respective method etc.
# . How many times a year its adjusted etc.
#
# Once initted the basket can be used to:
# - calculate the currency composition
# - calculate the increase and decrease in value based on other currencies.
# - calculate out of sample performance with every next period.
#
#
# Additional things
# - calculate optimal basket and performance difference
# - be able to combine baskets calculated over different time periods.
import os


import time
import sys

import pandas as pd

method = {'Manual': 10,
          'GDP': 50,
          'PP': 40,
          'GT': 0}

class Basket_Model:
    def __init__(self,
                 method_weights: dict,
                 adjusting_period: int,
                 price_data: pd.DataFrame,
                 start_date: time.datetime,
                 time_frame_GDP=15,
                 time_frame_PP=5,
                 time_frame_GT=10,
                 manual_weights=None,
                 min_basket_size=1,
                 n_currencies_pp=5,
                 weighted_pp=False):

        self.method_weights = method_weights
        self.adjusting_period = adjusting_period
        self.price_data = price_data
        self.start_date = start_date

        self.time_frame_GDP = time_frame_GDP
        self.time_frame_PP = time_frame_PP
        self.time_frame_GT = time_frame_GT
        self.manual_weights = manual_weights

        self.n_currencies = n_currencies_pp
        self.weighted = weighted_pp


    def fit(self):

        target_weights_dict = {}
        for method_key in self.method_weights.items():

            if method_key == 'Manual':
                print('determine target weights for final year')
                target_weights_dict_sample = self.manual_weights * self.method_weights[method_key]
            elif method_key == "GDP":
                target_weights_dict_sample = calc_weights_GDP(self.price_data, self.start_date, self.time_frame_GDP) \
                                             * self.method_weights[method_key]
                print('determine weights based on GDP')
            elif method_key == "PP":
                print('determine weights based on past time_frame price data performance')
                target_weights_dict_sample = calc_weights_PP(self.price_data, self.start_date, self.time_frame_PP,
                                                             self.n_currencies, self.weighted) \
                                             * self.method_weights[method_key]
            elif method_key == "GT":
                print('determine weights baded on % of use in gloval trade in time frame')
                target_weights_dict_sample = calc_weights_GT(self.price_data, self.start_date, self.time_frame_GDP) \
                                             * self.method_weights[method_key]
            else:
                print('method not found')
                sys.exit()

        for key in target_weights_dict_sample.keys():
            if key in target_weights_dict.keys():
                target_weights_dict[key] = target_weights_dict[key] + target_weights_dict_sample[key]

        return target_weights_dict


def calc_weights_GDP(data, date, timeframe_year):
    """
    Function to to calculate weights for a currency basket based on their % of the global economy

    Parameters
    ----------
    data : pd.Dataframe
        Pandas dataframe with years as rows and currencies as column filled with GDP data
    date : datetime
        Date from which to start the backwards test
    timeframe_year: int
        Number of years of backwards data to use

    Returns
    -------

    """
    start_year = (date - timeframe_year).year
    timeframe_slice = slice(start_year, date.year)

    data_summed_timeframe = data.iloc[timeframe_slice,:].sum(axis=0)
    weights = data_summed_timeframe/ sum(data_summed_timeframe) * 100

    target_weights_dict = {key : value for key, value in zip(weights.columns, weights)}

    return target_weights_dict


def calc_weights_PP(data, date, timeframe_year, n_currencies,
                    weighted=False):
    """
    Function to calculate the weights for a currency basket based on the price performance over a set timeframe.

    Parameters
    ----------
    data : pd.Dataframe
        Pandas dataframe with years as rows and currencies as column filled with price data
    date: datetime
        Date from which to start the backwards test
    timeframe_year : int
        Number of years of backwards data to use
    n_currencies
    weighted

    Returns
    -------

    """
    start_date = date - timeframe_year
    data_price_change = data.loc[date,:] - data.loc[start_date]
    top_price_changed = data_price_change.sort_values(0, axis=1, ascending=False).iloc[:, :n_currencies]

    if weighted:
        weights = top_price_changed / sum(top_price_changed) * 100
    else:
        weights = (top_price_changed/ top_price_changed) * 100/n_currencies

    target_weights_dict = {key : value for key, value in zip(weights.columns, weights)}

    return target_weights_dict


def calc_weights_GT(data, date, timeframe_year):
    """
    Function to to calculate weights for a currency basket based on their % of global trade

    Parameters
    ----------
    data : pd.Dataframe
        Pandas dataframe with years as rows and currencies as column filled with import export data
    date : datetime
        Date from which to start the backwards test
    timeframe_year: int
        Number of years of backwards data to use

    Returns
    -------

    """
    start_year = (date - timeframe_year).year
    timeframe_slice = slice(start_year, date.year)

    data_summed_timeframe = data.iloc[timeframe_slice,:].sum(axis=0)
    weights = data_summed_timeframe/ sum(data_summed_timeframe) * 100

    target_weights_dict = {key : value for key, value in zip(weights.columns, weights)}

    return target_weights_dict
