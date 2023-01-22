
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


import sys

import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

class Basket_Model:
    def __init__(self,
                 method_parameters: dict,
                 price_data: pd.DataFrame,
                 GDP_data : pd.DataFrame,
                 GT_data : pd.DataFrame,
                 start_date
                 ):

        self.method_parameters = method_parameters
        self.price_data = price_data
        self.GDP_data = GDP_data
        self.start_date = start_date


    def fit(self):

        target_weights_dict = {}
        for method_key in self.method_parameters.keys():

            if method_key == 'Manual':
                print('determine target weights for final year')
                parameters = self.method_parameters[method_key]
                target_weights_dict_sample = {}
                for currency in parameters['weights'].keys():
                    target_weights_dict_sample.update({currency: parameters['weights'][currency]/100 * 100/parameters['weight']})

            elif method_key == "GDP":
                print('determine weights based on GDP')
                parameters = self.method_parameters[method_key]
                target_weights_dict_sample = calc_weights_GDP(self.GDP_data, self.start_date, parameters['time_period'])
                for currency in target_weights_dict_sample.keys():
                    target_weights_dict_sample[currency] = target_weights_dict_sample[currency] * 100/parameters['weight']


            elif method_key == "PP":
                print('determine weights based on past time_frame price data performance')
                parameters = self.method_parameters[method_key]
                target_weights_dict_sample = calc_weights_PP(self.price_data, self.start_date, parameters['time_period'],
                                                             parameters['n_currncies'], parameters['weighted'])
                for currency in target_weights_dict_sample.keys():
                    target_weights_dict_sample[currency] = target_weights_dict_sample[currency] * 100/parameters['weight']

            elif method_key == "GT":
                print('determine weights baded on % of use in gloval trade in time frame')
                parameters = self.method_parameters[method_key]
                target_weights_dict_sample = calc_weights_GT(self.price_data, self.start_date, parameters['time_period'])
                for currency in target_weights_dict_sample.keys():
                    target_weights_dict_sample[currency] = target_weights_dict_sample[currency] * 100/parameters['weight']

            else:
                print('method not found')
                sys.exit()

        for key in target_weights_dict_sample.keys():
            if key in target_weights_dict.keys():
                target_weights_dict[key] = target_weights_dict[key] + target_weights_dict_sample[key]

        self.target_weights_dict = target_weights_dict


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
    start_year = (date - relativedelta(years=timeframe_year)).year
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
