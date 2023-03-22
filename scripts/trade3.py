import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data(code):
    df = ts.get_k_data(code)
    df.index = pd.to_datetime(df.date)
    df['close'] = df['close'].astype(float)
    return df


def get_macd(df, short=12, long=26, mid=9):
    """
    计算MACD指标
    """
    # 计算短期移动平均线EMA12
    EMA12 = pd.Series(df['close'].ewm(span=short).mean())
    # 计算长期移动平均线EMA26
    EMA26 = pd.Series(df['close'].ewm(span=long).mean())
    # 计算离差值DIF
    DIF = pd.Series(EMA12 - EMA26)
    # 计算DIF的9日移动平均DEA
    DEA = pd.Series(DIF.ewm(span=mid).mean())
    # 计算MACD指标
    MACD = pd.Series((DIF - DEA) * 2, name='MACD')
    return MACD


def get_tang(df, n=20):
    """
    计算唐奇安通道指标
    """
    Hn = df.high.rolling(n).max()
    Ln = df.low.rolling(n).min()

    up_line = Hn.shift(1)

    down_line = Ln.shift(1)

    return up_line, down_line


def plot_chart(df, up_line, down_line):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(df.close.values)

    ax.plot(up_line.values)

    ax.plot(down_line.values)

    plt.show()


if __name__ == '__main__':
    code = '605117'

    df = get_data(code)

    macd = get_macd(df)

    up_line, down_line = get_tang(df, n=20)

    plot_chart(df, up_line, down_line)