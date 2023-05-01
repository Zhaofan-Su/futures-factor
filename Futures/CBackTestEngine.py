import pandas as pd
import numpy as np
import math

# import self.log.logger
# from datetime import datetime, timedelta
from Config import Futures, PeriodList
from utils import str2datetime, build_trade_days

# 日志
from Logger import Logger

SamplePath = './SamplePool/'
DataPath = './database/'


class CBackTestEngine(object):

    def __init__(self, sdate, edate, log_name='all', commission=False,  leverage=True, portfolio_cash=10000000) -> None:
        self.log = Logger(log_name, level='debug')

        self.sdate = str2datetime(sdate)
        self.edate = str2datetime(edate)

        # 初始化账户信息及持仓
        self.init_portofolio(portfolio_cash)
        # 是否使用杠杆
        self.leverage = leverage
        # 是否使用手续费
        self.commission = commission

        # 交易标的
        self.transactions = []
        for exchange in Futures:
            for future in Futures[exchange]:
                self.transactions.append(f'{future}.{exchange}')
        # 交易日列表
        self.trade_days = build_trade_days(sdate, edate)
        # universe mask
        self.universe_mask = self.make_universe_mask()
        self.log.logger.info('Prepare the target future pool for each trade day succcessfully!')

        self.log.logger.info('The back test engine set successfully!')
        pass

    def init_portofolio(self, portfolio_cash=10000000) -> None:
        """ 初始化账户信息及持仓
        """
        # 持仓
        self.portfolio = {}
        self.portfolio['cash'] = portfolio_cash
        # 头寸
        self.position = {}
        self.log.logger.info('Init the portfolio and position detail successfully!')
        return

    def open_position(self, future_list: list) -> float:
        """ 开仓

        Args:
            future_list (list): 要开仓的品种的详情列表

        Returns:
            float: 开仓花费
        """
        cost = 0
        for future_detail in future_list:
            # 交易所
            exchange = future_detail['exchange']
            # 品种名称
            future = future_detail['future']

            # 加进持仓
            self.position[f'{future}.{exchange}'] = future_detail

            # 计算手续费
            if self.commission == False:
                commission = 0
            else:
                if Futures[exchange][future]['type'] == 1:
                    # 手续费按照比例计算
                    commission = Futures[exchange][future]['commission_price']
                else:
                    # 手续费按照固定价格计算
                    commission = Futures[exchange][future]['commission_price'] / (Futures[exchange][future]['trading_unit'] * future_detail['price'])

            self.log.logger.info(
                f'Open the {future_detail["direction"]} postion for {future}.{exchange}, the {future_detail["direction"]} price is {future_detail["price"]}, the commission is {commission}, the weight is {future_detail["weight"]}'
            )

            # 计算开仓手续费
            cost += commission * future_detail['weight']

        return cost

    def close_position(self, close_data: pd.Series) -> float:
        """ 平掉所有仓位

        Args:
            close_data (pd.Series): 品种的平仓价格

        Returns:
            float: 平仓收益率
        """
        # 平仓计算价格
        all_return = 0
        for holding in self.position.keys():
            holding_exchange = holding.split('.')[1]
            holding_future = holding.split('.')[0]
            holding_detail = self.position[holding]
            deposit = Futures[holding_exchange][holding_future]['deposit'] if self.leverage else 1
            # 计算手续费
            if self.commission == False:
                commission = 0
            else:
                if Futures[holding_exchange][holding_future]['type'] == 1:
                    # 手续费按照比例计算
                    commission = Futures[holding_exchange][holding_future]['commission_price']
                else:
                    # 手续费按照固定价格计算
                    commission = Futures[holding_exchange][holding_future]['commission_price'] / (Futures[holding_exchange][holding_future]['trading_unit'] * close_data[holding])

            if holding_detail['direction'] == 'long':
                # 多头持仓
                ret = (close_data[holding] - holding_detail['price']) / holding_detail['price'] / deposit
            elif holding_detail['direction'] == 'short':
                # 空头持仓
                ret = (holding_detail['price'] - close_data[holding]) / holding_detail['price'] / deposit
            self.log.logger.info(
                f'Close the position for {holding}, the holding price is {holding_detail["price"]}, the holding direction is {holding_detail["direction"]}, the close price is {close_data[holding]}, the return ratio is {ret}, the commission is {commission}'
            )

            # 计算平仓收益率
            if Futures[holding_exchange][holding_future]['bilateral']:
                # 手续费为双边，则计入手续费
                commission = commission * holding_detail['weight']
                all_return -= commission
            all_return += (ret * holding_detail['weight'])

        # 清空持仓
        self.position = {}
        return all_return

    def make_universe_mask(self) -> pd.DataFrame:
        """ 获取回测区间内每个品种是否在交易池中

        Returns:
            pd.DataFrame: universe_mask
        """
        all_false = np.full((len(self.trade_days), len(self.transactions)), False, dtype=bool)
        universe_mask = pd.DataFrame(all_false, index=self.trade_days, columns=self.transactions)

        for index, row in universe_mask.iterrows():
            date = index

            # 计算该日期的交易池在哪个文件中
            if date.month > 4:
                filename = f'{date.year}-05-01.{date.year+1}-04-30.csv'
            elif date.month <= 4:
                filename = f'{date.year-1}-05-01.{date.year}-04-30.csv'

            samples = pd.read_csv(f'{SamplePath}{filename}', index_col=0)
            sample_codes = samples['future'].str.cat(samples['exchange'], sep='.').values
            row[sample_codes] = True

        return universe_mask

    def get_data(self, data_item: str) -> pd.DataFrame:
        """ 获取指定交易日所有合约的交易数据

        Args:
            data_item (str): 交易数据代码

        Returns:
            pd.DataFrame: _description_
        """
        data_df = pd.DataFrame(index=self.trade_days, columns=self.transactions)
        for exchange in Futures:
            for future in Futures[exchange]:
                future_all_data = pd.read_excel(f'{DataPath}{exchange}/{future}.{exchange}.xlsx', index_col=0)
                future_dates = list(set(self.trade_days).intersection(future_all_data.index.to_list()))
                future_use_data = future_all_data.loc[future_dates, :]
                future_item_data = future_use_data[data_item]

                data_df.loc[future_dates, f'{future}.{exchange}'] = future_item_data

        # 对整张数据表使用universe_mask进行过滤
        data_df[self.universe_mask == False] = np.nan

        return pd.DataFrame(data_df, dtype=float)

    def trade_by_rank(self, factor_values: pd.DataFrame, weight_type='equal', reverse=False) -> pd.Series:
        """ 多空因子值排名前后20%的品种

        Args:
            factor_values (pd.DataFrame): _description_
            weight_type (str): 加权方式, 'equal'为等权, 'sort'为按排名归一化加权
            reverse (bool): 是否将因子反转

        Returns:
            pd.Series: 每个交易日的单日收益
        """

        return_df = pd.Series(index=factor_values.index[1:-1], dtype=float)

        # 每天的收盘价
        close_data = self.get_data('active_con_close')
        # 等权，每天做多前20%，做空后20%，T+1平仓
        for idx in range(1, len(factor_values) - 1):
            ret = 0
            # T-1天
            tdate = factor_values.index[idx - 1]
            # T天，当天
            date = factor_values.index[idx]
            self.log.logger.info(f'The trade on {date} has started!')

            # t-1天可以交易的品种及数量
            choose_futures = ~np.isnan(factor_values.loc[tdate, :]) & self.universe_mask.loc[tdate, :]
            tdate_futures = factor_values.columns[choose_futures]
            tdate_future_nums = len(tdate_futures)
            if tdate_future_nums <= 1:
                self.log.logger.info(f'The trade on {date} has ended!')
                return_df[date] = ret
                continue

            # t-1天可以交易的期货的因子值
            tdate_values = factor_values.loc[date, tdate_futures]
            # 升序排序
            # temp = np.sort(tdate_values.values)
            temp = np.sort(tdate_values)
            # ini_index = np.argsort(temp)
            ini_index = np.argsort(tdate_values)
            sort_weight = np.abs(ini_index + 1) / np.abs(ini_index + 1).sum()

            # 平仓
            close_ret = self.close_position(close_data.loc[date, :])
            # 做空
            short_futures = tdate_futures[ini_index[0:math.floor(tdate_future_nums * 0.2)]]
            # 做多
            long_futures = tdate_futures[ini_index[-math.floor(tdate_future_nums * 0.2):]]

            if reverse:
                # 将因子反转
                temp_futures = short_futures
                short_futures = long_futures
                long_futures = temp_futures

            # 空头开仓
            short_details = []
            for short in short_futures:
                # 等权
                if weight_type == 'equal':
                    weight = 1 / (len(short_futures) + len(long_futures))
                elif weight_type == 'sort':
                    weight = sort_weight[short]
                short_exchange = short.split('.')[1]
                short_future = short.split('.')[0]

                detail = {'direction': 'short', 'exchange': short_exchange, 'future': short_future, 'price': close_data.at[date, short], 'weight': weight}
                short_details.append(detail)
            short_cost = self.open_position(short_details)

            # 多头开仓信息
            long_details = []
            for long in long_futures:
                # 等权
                if weight_type == 'equal':
                    weight = 1 / (len(short_futures) + len(long_futures))
                elif weight_type == 'sort':
                    weight = sort_weight[long]
                long_exchange = long.split('.')[1]
                long_future = long.split('.')[0]

                long_detail = {'direction': 'long', 'exchange': long_exchange, 'future': long_future, 'price': close_data.at[date, long], 'weight': weight}
                long_details.append(long_detail)
            long_cost = self.open_position(long_details)

            # 当日收益, 平仓收益-开仓成本
            ret = close_ret - short_cost - long_cost
            return_df[date] = ret
            self.log.logger.info(f'The return for {date} is {ret}')
            self.log.logger.info(f'The trade on {date} has ended!')
        return return_df

    def trade_by_ts_rule_factor(self, factor_values: pd.DataFrame, volatility_df: pd.DataFrame, reverse=False) -> pd.Series:
        """ 时序规则因子回测，使用波动率加权

        Args:
            factor_values (pd.DataFrame): 因子值
            volatility_df (pd.DataFrame): 波动率序列
            reverse (bool): 是否对因子进行反转

        Returns:
            pd.Series: 单日收益率序列
        """

        return_df = pd.Series(index=factor_values.index[1:-1], dtype=float)

        # 每天的收盘价
        close_data = self.get_data('active_con_close')
        # 波动率加权，做多为True的，做空为False的
        for idx in range(1, len(factor_values) - 1):
            daily_ret = 0
            # T-1天
            tdate = factor_values.index[idx - 1]
            # T天，当天
            date = factor_values.index[idx]
            self.log.logger.info(f'The trade on {date} has started!')

            # t-1天可以交易的品种及数量
            choose_futures = ~np.isnan(factor_values.loc[tdate, :]) & self.universe_mask.loc[tdate, :]
            tdate_futures = factor_values.columns[choose_futures]
            # t-1天可交易品种的波动率序列
            tdate_volatility = volatility_df.loc[date, choose_futures]
            tdate_weights = (1 / tdate_volatility) / (1 / tdate_volatility).abs().sum()
            # 做多
            long_futures = tdate_futures[factor_values.loc[tdate, tdate_futures]]
            # 做空
            short_futures = tdate_futures[~factor_values.loc[tdate, tdate_futures]]
            if reverse:
                temp = short_futures
                short_futures = long_futures
                long_futures = temp
            # 平仓收益
            close_ret = self.close_position(close_data.loc[date, :])

            # 空头开仓
            short_details = []
            for short in short_futures:
                short_exchange = short.split('.')[1]
                short_future = short.split('.')[0]

                short_detail = {'direction': 'short', 'exchange': short_exchange, 'future': short_future, 'price': close_data.at[date, short], 'weight': tdate_weights[short]}
                short_details.append(short_detail)
            short_pay = self.open_position(short_details)

            # 多头开仓
            long_details = []
            for long in long_futures:
                long_exchange = long.split('.')[1]
                long_future = long.split('.')[0]

                long_detail = {'direction': 'long', 'exchange': long_exchange, 'future': long_future, 'price': close_data.at[date, long], 'weight': tdate_weights[long]}
                long_details.append(long_detail)
            long_pay = self.open_position(long_details)

            # 当日收益, 平仓收益减去开仓成本
            daily_ret = close_ret - short_pay - long_pay
            return_df[date] = daily_ret
            self.log.logger.info(f'The return for {date} is {daily_ret}')
            self.log.logger.info(f'The trade on {date} has ended!')

        return return_df

    def trade_by_ts_mome_factor(self, factor_values: pd.DataFrame, reverse=False) -> pd.Series:
        """ 时序动量回测

        Args:
            factor_values (pd.DataFrame): 因子值

        Returns:
            pd.Series: 单日收益率序列
        """
        return_df = pd.Series(index=factor_values.index[1:-1], dtype=float)

        # 每天的收盘价
        close_data = self.get_data('active_con_close')
        # 因子值加权，做多因子为正的，做空因子为负的
        for idx in range(1, len(factor_values) - 1):
            daily_ret = 0
            # T-1天
            tdate = factor_values.index[idx - 1]
            # T天，当天
            date = factor_values.index[idx]
            self.log.logger.info(f'The trade on {date} has started!')

            # t-1天可以交易的品种及数量
            choose_futures = ~np.isnan(factor_values.loc[tdate, :]) & self.universe_mask.loc[tdate, :]
            tdate_futures = factor_values.columns[choose_futures]
            # t-1天可交易品种的因子值
            tfactor_value = factor_values.loc[date, choose_futures]
            tdate_weights = tfactor_value.abs() / tfactor_value.abs().sum()
            # 做多
            long_futures = tdate_futures[factor_values.loc[tdate, tdate_futures] > 0]
            # 做空
            short_futures = tdate_futures[factor_values.loc[tdate, tdate_futures] < 0]
            if reverse:
                temp = short_futures
                short_futures = long_futures
                long_futures = temp
            # 平仓收益
            close_ret = self.close_position(close_data.loc[date, :])

            # 空头开仓
            short_details = []
            for short in short_futures:
                short_exchange = short.split('.')[1]
                short_future = short.split('.')[0]

                short_detail = {'direction': 'short', 'exchange': short_exchange, 'future': short_future, 'price': close_data.at[date, short], 'weight': tdate_weights[short]}
                short_details.append(short_detail)
            short_pay = self.open_position(short_details)

            # 多头开仓
            long_details = []
            for long in long_futures:
                long_exchange = long.split('.')[1]
                long_future = long.split('.')[0]

                long_detail = {'direction': 'long', 'exchange': long_exchange, 'future': long_future, 'price': close_data.at[date, long], 'weight': tdate_weights[long]}
                long_details.append(long_detail)
            long_pay = self.open_position(long_details)

            # 当日收益, 平仓收益-开仓成本
            daily_ret = close_ret - short_pay - long_pay
            return_df[date] = daily_ret
            self.log.logger.info(f'The return for {date} is {daily_ret}')
            self.log.logger.info(f'The trade on {date} has ended!')

        return return_df

    