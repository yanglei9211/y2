import datetime

import tushare as ts
import pandas as pd
import numpy as np

# 设置token
ts.set_token('')

# 获取605117这只股票的历史数据
df = ts.pro_bar(ts_code='300015.SZ', adj='qfq', start_date='20200101', end_date='20220322')

# 计算20日均线和60日均线
df['ma5'] = df['close'].rolling(window=20).mean()
df['ma20'] = df['close'].rolling(window=60).mean()

# 判断买入或卖出信号
# if df.iloc[-1]['ma20'] > df.iloc[-1]['ma60']:
#     print('买入信号')
# else:
#     print('卖出信号')

i = 0
now = datetime.datetime.now()
for i in range(1, 100):
    print(i, df.iloc[-i]['ma5'],df.iloc[-i]['ma20'])
    if df.iloc[-i]['ma5'] > df.iloc[-i]['ma20']:
        print(now - datetime.timedelta(i), '买入信号')
    else:
        print(now - datetime.timedelta(i), '卖出信号')