from pprint import pprint

import tushare as ts
import pandas as pd
import numpy as np

def count_bs(code, dt):
    # 获取605117的历史数据
    # df = ts.get_k_data('600036', start='2022-01-01')
    df = ts.get_k_data(code, start=dt)

    # 计算唐奇安通道
    n = 20
    df['high_roll'] = df['high'].rolling(n).max()
    df['low_roll'] = df['low'].rolling(n).min()
    df['mid'] = (df['high_roll'] + df['low_roll']) / 2

    # 计算EMA12和EMA26
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()

    # 计算DIF和DEA
    dif = ema12 - ema26
    dea = dif.ewm(span=9).mean()

    # 计算MACD指标
    macd = (dif - dea) * 2

    # 计算买入和卖出信号
    df['signal'] = np.where((dif > dea) & (dif.shift() < dea.shift()), 1, 0)
    df['signal'] = np.where((dif < dea) & (dif.shift() > dea.shift()), -1, df['signal'])

    # 计算每天触发卖点或买点时的价格
    buy_price_list = []
    sell_price_list = []
    for i in range(1, len(df)):
        if df.iloc[i]['signal'] == 1 and df.iloc[i-1]['signal'] == 0:
            buy_price_list.append((df.iloc[i]['date'], df.iloc[i]['open']))
        elif df.iloc[i]['signal'] == -1 and df.iloc[i-1]['signal'] == 0:
            sell_price_list.append((df.iloc[i]['date'], df.iloc[i]['open']))

    print("买入日期和价格：")
    pprint(buy_price_list)
    print("卖出日期和价格：")
    pprint(sell_price_list)
    return buy_price_list, sell_price_list

def calculate_return(buy_dates, sell_dates):
    total_profit = 0
    idxb, idxs = 0, 0
    while idxb < len(buy_dates) and idxs < len(sell_dates):
        buy_date = buy_dates[idxb][0]
        buy_price = buy_dates[idxb][1]
        sell_date = sell_dates[idxs][0]
        sell_price = sell_dates[idxs][1]
        if buy_date < sell_date:
            print(buy_date, sell_date, buy_price, sell_price, sell_price - buy_price)
            profit = (sell_price - buy_price) / buy_price
            total_profit += profit
            idxb+=1
            idxs+=1
        else:
            idxs+=1
    # for i in range(len(buy_dates)):
    #
    #     buy_date = buy_dates[i][0]
    #     buy_price = buy_dates[i][1]
    #     sell_date = sell_dates[i][0]
    #     sell_price = sell_dates[i][1]
    #     print(buy_date, sell_date, buy_price, sell_price, sell_price-buy_price)
    #     profit = (sell_price - buy_price) / buy_price
    #     total_profit += profit
    return total_profit / len(buy_dates)


bb,ss = count_bs('605117', '2022-01-01')
print(calculate_return(bb,ss))