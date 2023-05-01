from datetime import timedelta, datetime
from chinese_calendar import is_workday
from Config import PeriodList
import pandas as pd

def str2datetime(date_str: str) -> datetime:
    """ 将字符串时间转为datetime

    Args:
        date_str (str): 字符串时间

    Returns:
        datetime: 时间戳
    """
    dtime = datetime.strptime(date_str, "%Y-%m-%d")
    return dtime


def find_recent_trade_day(date: datetime) -> datetime:
    """ 寻找离某个时间点最近的交易日
        如果该时间点为交易日，则返回该时间点
        否则，往前寻找

    Args:
        date (time): 时间点

    Returns:
        time: 离该时间点最近的交易日
    """

    while True:
        if is_trade_day(date):
            break
        else:
            date = date - timedelta(days=1)

    return date


def is_trade_day(date: datetime) -> bool:
    """ 判断某个日期是否为交易日

    Args:
        date (datetime): 具体日期

    """
    if is_workday(date):
        if date.isoweekday() < 6:
            return True
    return False

def build_dataset(data_item:str) -> pd.DataFrame:
    """ 获取指定时间的

    Args:
        data_item (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return

def build_trade_days(sdate:str, edate:str) -> list:
    """ 获取从sdate到edate之间的交易日  Args:
        sdate (str): 开始时间
        edate (str): 截止时间

    Returns:
        list: 日期列表
    """
    date_list = []
    sdate = str2datetime(sdate)
    edate = str2datetime(edate)
    now_date = sdate
    flag = False
    while flag == False:
        if now_date == edate:
            flag = True
        if is_trade_day(now_date):
            date_list.append(datetime.strptime(now_date.strftime("%Y-%m-%d"), "%Y-%m-%d"))
        now_date = now_date + timedelta(days=1)
    
    return date_list
        