import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from src.silk_basket.utils import transfer_date_to_datetime
from src.silk_basket.model import Basket_Model

if __name__ == "__main__" :

    data_path = 'C:\scrt_projs\silk_peg\src\silk_peg\example\data'

    price_data_df = transfer_date_to_datetime(
        pd.read_excel(os.path.join(data_path, 'price.xlsx'), header=1),
        'Year', format='%YYYY%mm%dd')
    gdp_data_df = transfer_date_to_datetime(
        pd.read_excel(os.path.join(data_path, 'GDP.xlsx'), header=0),
        'time', format='%YYYY%mm%dd').replace([' NaN '],0)


    price_change_data_df = price_data_df.pct_change()

    method = {'Manual': {"weight": 10, 'time_period': 0, 'weights': {'Bitcoin': 50, 'Gold': 50}},
              'GDP': {"weight": 50, 'time_period': 15, 'min_contribution': 1},
              'PP': {"weight": 40, 'time_period': 5, 'weighted': False, 'n_currencies': 5},
              'GT': {"weight": 0, 'time_period': 10, 'min_contribution': 5}}

    model = Basket_Model(method, price_data_df, gdp_data_df, pd.DataFrame(), datetime.datetime.now())
    model.fit()


    # currency_country_LUT = {'USDUSD': 'USA', 'CNYUSD': 'China', 'EURUSD': 'EU', 'JPYUSD': 'Japan', 'GBPUSD': 'UK',
    #                         'INRUSD': 'India', 'CADUSD' : 'Canada', 'KRWUSD':'S. Korea', 'RUBUSD': 'Russia', 'BRLUSD': 'Brazil',
    #                         'AUDUSD': 'Australia', 'IDRUSD': 'Indonesia', 'CHFUSD': 'Switzerland', 'TRYUSD': 'Turkey',
    #                         'SEKUSD': 'Sweden', 'NOKUSD': 'Norway', 'SGDUSD':'Singapore','GOLD' : 'GOLD', 'Bitcoin':'Bitcoin'}
    # country_currency_LUT = {v: k for k, v in currency_country_LUT.items()}
    #
    # gdp_perc = calc_perc_row(gdp_data_df)
    # gdp_capita_perc = calc_perc_row(gdp_capita_data_df)
    #
    # price_moving_average = calc_ma(price_data_df, window=30)
    #
    # benchmark_devision = gdp_perc.drop('Total', axis=1)
    # benchmark_devision = benchmark_devision*0.95
    # benchmark_devision['GOLD'] = [2.5 for i in benchmark_devision.index]
    # benchmark_devision['Bitcoin'] = [2.5 for i in benchmark_devision.index]
    # benchmark_devision = benchmark_devision.loc[benchmark_devision.index.repeat(11)]
    # benchmark_devision = benchmark_devision.iloc[385:,:]
    #
    # new_value = []
    # benchmark_price = []
    # for (timestamp_row, row), i_row in zip(benchmark_devision.iterrows(), range(len(benchmark_devision)) ):
    #     if not i_row == 0:
    #         old_row = new_df.iloc[i_row-1,:]
    #     else:
    #         old_row = pd.Series([1 for i in range(len(row))], index=row.index)
    #         new_df = pd.DataFrame(columns=row.index)
    #
    #     country_columns = [country_currency_LUT[currency] for currency in row.index]
    #     new_row = price_change_data_df[country_columns].iloc[i_row + 1,:].values * old_row/100
    #     # new_value.append(old_value * np.nanmean((price_change_data_df[country_columns].iloc[i_row + 1,:].values * row.values)))
    #
    #     new_df = new_df.append(new_row, ignore_index=True)
    #     benchmark_price.append(new_row.sum(skipna=True))
    #
    #
    # # benchmark = gdp_perc*price_data_df
    #
    # fig, axs = plt.subplots()
    # # axs.plot(price_data_df['EURUSD']/price_data_df['EURUSD'].mean())
    # # axs.plot(price_data_df['JPYUSD']/price_data_df['JPYUSD'].mean())
    #
    # # axs.plot(price_moving_average['EURUSD'].iloc[:-6].index, new_value)
    # axs.plot(price_moving_average['EURUSD'].iloc[:-6].index, benchmark_price)
    # plt.show()
    #
    #
    # print('finito')