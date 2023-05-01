from factor_pool import pn_mome, ts_rule_mome, ts_mome, warehouse_receipt, term_structure
from factor_weights import get_volatility_df
from CBackTestEngine import CBackTestEngine

from Config import PeriodList, SDate, EDate, Future_Dic
from utils import build_trade_days

import logging
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

if __name__ == '__main__':
    filename = 'ts_mome_120d'
    bt_engine = CBackTestEngine(sdate=SDate, edate=EDate, log_name=filename, leverage=True)

    close_data = bt_engine.get_data('active_con_close')

    # 截面动量因子回测
    # factor_value = pn_mome(close_data, period=20)
    # factor_value = pn_mome(close_data, period=3)
    # return_list = bt_engine.trade_by_rank(factor_value, reverse=False)

    # 时序规则因子测试
    # factor_value = ts_rule_mome(close_data, 10, 20)
    # factor_value = ts_rule_mome(close_data, 60, 120)
    # volatility_df = get_volatility_df(close_data, 60)
    # return_list = bt_engine.trade_by_ts_rule_factor(factor_value, volatility_df, reverse=False)

    # 周期时序动量因子
    factor_value = ts_mome(close_data, 120)
    # factor_value = ts_mome(close_data, 60)
    return_list = bt_engine.trade_by_ts_mome_factor(factor_value, reverse=False)

    # 仓单因子
    # warehouse_df = pd.read_excel('./database/warehouse.xlsx', index_col=0)
    # trade_days = build_trade_days(SDate, EDate)
    # warehouse_df = warehouse_df.loc[trade_days, :]
    # factor_value = warehouse_receipt(warehouse_df, 52)
    # return_list = bt_engine.trade_by_rank(-factor_value, reverse=False)

    # 期限因子
    # price = pd.read_excel('./database/main_second_close.xlsx', index_col=0)
    # trade_days = build_trade_days(SDate, EDate)
    # price = price.loc[trade_days, :]
    # last_trade_day = pd.read_excel('./database/main_second_ltd.xlsx', index_col=0)
    # factor_value = term_structure(price, last_trade_day, Future_Dic)
    # return_list = bt_engine.trade_by_rank(factor_value, 'sort', reverse=False)

    # 年化收益率
    ret_y = return_list.mean() * 252
    bt_engine.log.logger.info(f'The annual rate of return for {filename} is {ret_y}.')
    # 波动率
    volatility = return_list.std() * np.sqrt(252)
    bt_engine.log.logger.info(f'The annual volatility rate for {filename} is {volatility}.')
    # 夏普比率
    sharp = (ret_y - 0.0214) / volatility
    bt_engine.log.logger.info(f'The annual sharp ratio for {filename} is {sharp}.')

    plt.figure(figsize=(12, 8))
    # plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('date')
    plt.ylabel('return')
    plt.plot(return_list.index, return_list.cumsum())
    plt.title(filename)
    plt.savefig(f'./figs/{filename}.png')
    plt.show()
