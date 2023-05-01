import pandas as pd
import numpy as np


# 波动率序列
def get_volatility_df(data: pd.DataFrame, volatility_period: 60) -> pd.DataFrame:
    """ 年化波动率加权

    Args:
        data (pd.DataFrame): 数据
        volatility_period (60): 波动率周期

    Returns:
        pd.DataFrame: n days * m futures，每天每个品种的波动率
    """

    # 波动率序列
    volatility_df = data.pct_change().rolling(volatility_period).std() * np.sqrt(volatility_period)
    volatility_df.fillna(method='bfill', inplace=True)

    return volatility_df