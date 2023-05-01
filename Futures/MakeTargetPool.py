import pandas as pd
import numpy as np
from Config import PeriodList, Future_Dic
from utils import str2datetime, find_recent_trade_day
import logging
from Logger import initLogConf

initLogConf()

DataPath = './database/'
SamplePath = './SamplePool/'

for period in PeriodList:
    logging.info(
        f'Start to choose the sample futures for the period from {period[0]} to {period[1]}'
    )
    sample_file_name = f'{period[0]}.{period[1]}.csv'
    sample_pool = {'exchange': [], 'future': []}

    sdate = str2datetime(period[0])
    edate = str2datetime(period[1])

    recent_trade_day = find_recent_trade_day(edate)

    for exchange in Future_Dic:
        for future in Future_Dic[exchange]:
            logging.info(
                f'{period[0]} to {period[1]}, {future}.{exchange} is checking...'
            )
            # 品种的上市时间
            future_to_market = str2datetime(Future_Dic[exchange][future]['time_to_market'])
            # 是否在考察节点前一年上市
            days_delta = (edate - future_to_market).days
            if days_delta < 365:
                # 该品种排除出此考察期间
                continue

            # 读取品种数据
            future_data = pd.read_excel(
                f'{DataPath}{exchange}/{future}.{exchange}.xlsx')

            row = future_data[future_data.date ==
                              recent_trade_day].index.tolist()[0]
            future_60_data = future_data.loc[row - 59:row]
            future_20_data = future_data.loc[row - 19:row]

            # 成交额单位为 万元
            if np.all(future_60_data.amount >= 100000) and np.all(
                    future_60_data.active_con_volume >= 100000) and np.all(
                        future_20_data.amount >= 10000) and np.all(
                            future_20_data.active_con_volume >= 1000):
                sample_pool['exchange'].append(exchange)
                sample_pool['future'].append(future)

    sample_pool = pd.DataFrame(sample_pool)
    sample_pool.to_csv(f'{SamplePath}{sample_file_name}')
    logging.info(
        f'The sample pool from {period[0]} to {period[1]} has been saved!')
