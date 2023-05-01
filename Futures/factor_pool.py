import pandas as pd
import numpy as np
from factor_weights import get_volatility_df


def pn_mome(data: pd.DataFrame, period: int) -> pd.DataFrame:
    """ 周期截面动量因子

    Args:
        period (int): 周期长短，短周期为20，长周期为120

    Returns:
        pd.DataFrame: 因子值dataframe，每行为一天，每列为一个品种
    """
    ret_data = data.apply(lambda x: np.log(x).diff(1), axis=0)

    factor_value = ret_data.apply(lambda x: x.rolling(period).sum())

    return factor_value


def ts_rule_mome(data: pd.DataFrame, short_period: int, long_period: int, volatility_period=60) -> pd.DataFrame:
    """ 周期时序规则动量因子

    Args:
        short_period (int): 短周期
        long_period (int): 长周期
        volatility_period (int): 波动率周期

    Returns:
        pd.DataFrame: 因子值
    """

    short_ma = data.apply(lambda x: x.rolling(short_period).mean(), axis=0)
    long_ma = data.apply(lambda x: x.rolling(long_period).mean())
    factor_value = short_ma >= long_ma

    return factor_value


def ts_mome(data: pd.DataFrame, period: int) -> pd.DataFrame:
    """ 周期时序动量因子

    Args:
        data (pd.DataFrame): _description_
        period (int): 周期

    Returns:
        pd.DataFrame: _description_
    """
    ret_df = data.pct_change()
    volatility_df = get_volatility_df(data, period)
    volatility_df = volatility_df.apply(lambda x: np.square(x), axis=0)
    factor_value = ret_df.rolling(period).sum().div(volatility_df)

    return factor_value


def warehouse_receipt(data: pd.DataFrame, period: int, fre='w') -> pd.DataFrame:
    """ 仓单因子

    Args:
        data (pd.DataFrame): 仓单数据
        period (int): 计算周期
        fre (str, optional): _description_. 'd' means day, 'w' means week, 'm' means month, 'y' means year

    Returns:
        pd.DataFrame: _description_
    """
    if fre == 'd':
        days = period
    if fre == 'w':
        days = period * 5
    if fre == 'm':
        days = period * 20
    if fre == 'y':
        days = period * 252

    factor_value = data.pct_change(days)
    return factor_value


def term_structure(price: pd.DataFrame, last_trade_day: pd.DataFrame, future_dic: dict) -> pd.DataFrame:
    """ 期限结构因子

    Args:
        price (pd.DataFrame): 不同期限结构的价格
        last_trade_day (pd.DataFrame): 不同期限结构的最后交易日
        future_dic (dict): 期货

    Returns:
        pd.DataFrame: 因子值
    """
    # 近月合约
    near = []
    # 远月合约
    far = []
    futures = []
    for exchange in future_dic.keys():
        for future in future_dic[exchange]:
            near.append(f'{future}00.{exchange}')
            far.append(f'{future}01.{exchange}')
            futures.append(f'{future}.{exchange}')

    price_near = price.loc[:, near].apply(lambda x: np.log(x), axis=0)
    price_near.columns = futures
    price_far = price.loc[:, far].apply(lambda x: np.log(x), axis=0)
    price_far.columns = futures

    time_delta = last_trade_day.apply(lambda x: x - last_trade_day.index, axis=0)
    time_delta = time_delta.applymap(lambda x: x.days)
    time_delta_near = time_delta.loc[:, near]
    time_delta_far = time_delta.loc[:, far]
    time_delta_near.columns = futures
    time_delta_far.columns = futures

    factor_value = -(price_far - price_near).div(time_delta_far - time_delta_near) * 365

    return factor_value
