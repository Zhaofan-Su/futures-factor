# 回测区间
SDate = '2015-01-04'
EDate = '2022-01-04'
# 考察区间
PeriodList = [['2015-01-04', '2015-04-30'], ['2015-05-01', '2016-04-30'],
              ['2016-05-01', '2017-04-30'], ['2017-05-01', '2018-04-30'],
              ['2018-05-01', '2019-04-30'], ['2019-05-01', '2020-04-30'],
              ['2020-05-01', '2021-04-30'], ['2021-05-01', '2022-04-30']]

# 交易所-品种
Future_Dic = {
    "SHF": [
        "CU", "AL", "ZN", "AU", "AG", "RB", "FU", "RU", "BU", "HC", "NI", "SN",
        "SP", "SS"
    ],
    "INE": ["SC"],
    "DCE": [
        "C", "A", "B", "M", "Y", "P", "L", "V", "J", "JM", "I", "JD", "PP",
        "CS", "EG", "EB", "PG"
    ],
    "CZC": [
        "CF", "SR", "TA", "OI", "MA", "FG", "RM", "SF", "SM", "ZC", "AP", "UR",
        "SA"
    ]
}



# 各品种情况
# type： 0，按手数付费；1，按合约价值付费
# bilateral：是否为双边手续费
# time_to_market：何时上市
# commission_price：手续费基本价格
# trading_unit：每手合约交易单位
# deposit：保证金比例
Futures = {
    "SHF": {
        "CU": {
            'type': 1,
            'commission_price': 0.0005,
            'bilateral': True,
            'time_to_market': '1993-03-31',
            'trading_unit': 5,
            'deposit':0.12
        },
        "AL": {
            'type': 0,
            'commission_price': 15,
            'bilateral': True,
            'time_to_market': '1992-05-28',
            'trading_unit': 5,
            'deposit':0.12
        },
        "ZN": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '2007-03-26',
            'trading_unit': 5,
            'deposit':0.14
        },
        "AU": {
            'type': 0,
            'commission_price': 10,
            'bilateral': False,
            'time_to_market': '2008-01-09',
            'trading_unit': 1000,
            'deposit':0.10
        },
        "AG": {
            'type': 1,
            'commission_price': 0.00005,
            'bilateral': True,
            'time_to_market': '2012-05-10',
            'trading_unit': 15,
            'deposit':0.12
        },
        "RB": {
            'type': 1,
            'commission_price': 0.0005,
            'bilateral': True,
            'time_to_market': '2008-01-09',
            'trading_unit': 10,
            'deposit':0.13
        },
        "FU": {
            'type': 1,
            'commission_price': 0.00005,
            'bilateral': False,
            'time_to_market': '2004-08-25',
            'trading_unit': 10,
            'deposit':0.15
        },
        "RU": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '1993-11-25',
            'trading_unit': 10,
            'deposit':0.10
        },
        "BU": {
            'type': 1,
            'commission_price': 0.0005,
            'bilateral': True,
            'time_to_market': '2013-10-09',
            'trading_unit': 10,
            'deposit':0.15
        },
        "HC": {
            'type': 1,
            'commission_price': 0.0005,
            'bilateral': True,
            'time_to_market': '2014-03-21',
            'trading_unit': 10,
            'deposit':0.13
        },
        "NI": {
            'type': 0,
            'commission_price': 15,
            'bilateral': True,
            'time_to_market': '2015-03-27',
            'trading_unit': 1,
            'deposit':0.19
        },
        "SN": {
            'type': 0,
            'commission_price': 15,
            'bilateral': True,
            'time_to_market': '2015-03-27',
            'trading_unit': 1,
            'deposit':0.14
        },
        "SP": {
            'type': 1,
            'commission_price': 0.00025,
            'bilateral': False,
            'time_to_market': '2018-11-27',
            'trading_unit': 10,
            'deposit':0.15
        },
        "SS": {
            'type': 0,
            'commission_price': 10,
            'bilateral': False,
            'time_to_market': '2019-09-25',
            'trading_unit': 5,
            'deposit':0.14
        }
    },
    "INE": {
        "SC": {
            'type': 0,
            'commission_price': 100,
            'bilateral': False,
            'time_to_market': '2018-03-26',
            'trading_unit': 1000,
            'deposit':0.15
        }
    },
    "DCE": {
        "C": {
            'type': 0,
            'commission_price': 6,
            'bilateral': True,
            'time_to_market': '2004-9-22',
            'trading_unit': 10,
            'deposit':0.12
        },
        "A": {
            'type': 0,
            'commission_price': 10,
            'bilateral': True,
            'time_to_market': '2002-03-15',
            'trading_unit': 10,
            'deposit':0.12
        },
        "B": {
            'type': 0,
            'commission_price': 5,
            'bilateral': True,
            'time_to_market': '2004-12-22',
            'trading_unit': 10,
            'deposit':0.09
        },
        "M": {
            'type': 0,
            'commission_price': 7.5,
            'bilateral': True,
            'time_to_market': '2000-07-17',
            'trading_unit': 10,
            'deposit':0.1
        },
        "Y": {
            'type': 0,
            'commission_price': 12.5,
            'bilateral': True,
            'time_to_market': '2006-01-09',
            'trading_unit': 10,
            'deposit':0.09
        },
        "P": {
            'type': 0,
            'commission_price': 12.5,
            'bilateral': True,
            'time_to_market': '2007-10-29',
            'trading_unit': 10,
            'deposit':0.12
        },
        "L": {
            'type': 0,
            'commission_price': 5,
            'bilateral': True,
            'time_to_market': '2007-07-31',
            'trading_unit': 5,
            'deposit':0.11
        },
        "V": {
            'type': 0,
            'commission_price': 5,
            'bilateral': True,
            'time_to_market': '2009-05-25',
            'trading_unit': 5,
            'deposit':0.11
        },
        "J": {
            'type': 1,
            'commission_price': 0.0006,
            'bilateral': True,
            'time_to_market': '2011-04-15',
            'trading_unit': 100,
            'deposit':0.20
        },
        "JM": {
            'type': 1,
            'commission_price': 0.0006,
            'bilateral': True,
            'time_to_market': '2013-03-22',
            'trading_unit': 60,
            'deposit':0.20
        },
        "I": {
            'type': 1,
            'commission_price': 0.0005,
            'bilateral': True,
            'time_to_market': '2013-10-18',
            'trading_unit': 100,
            'deposit':0.13
        },
        "JD": {
            'type': 1,
            'commission_price': 0.00075,
            'bilateral': True,
            'time_to_market': '2013-11-08',
            'trading_unit': 5,
            'deposit':0.09
        },
        "PP": {
            'type': 0,
            'commission_price': 5,
            'bilateral': True,
            'time_to_market': '2014-02-28',
            'trading_unit': 5,
            'deposit':0.11
        },
        "CS": {
            'type': 0,
            'commission_price': 7.5,
            'bilateral': True,
            'time_to_market': '2014-12-19',
            'trading_unit': 10,
            'deposit':0.09
        },
        "EG": {
            'type': 0,
            'commission_price': 15,
            'bilateral': True,
            'time_to_market': '2018-12-10',
            'trading_unit': 10,
            'deposit':0.12
        },
        "EB": {
            'type': 0,
            'commission_price': 15,
            'bilateral': True,
            'time_to_market': '2019-09-26',
            'trading_unit': 5,
            'deposit':0.12
        },
        "PG": {
            'type': 0,
            'commission_price': 30,
            'bilateral': True,
            'time_to_market': '2020-03-30',
            'trading_unit': 20,
            'deposit':0.13
        }
    },
    "CZC": {
        "CF": {
            'type': 0,
            'commission_price': 21.5,
            'bilateral': False,
            'time_to_market': '2004-06-01',
            'trading_unit': 5,
            'deposit':0.07
        },
        "SR": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '2006-01-06',
            'trading_unit': 10,
            'deposit':0.07
        },
        "TA": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '2006-12-18',
            'trading_unit': 5,
            'deposit':0.07
        },
        "OI": {
            'type': 0,
            'commission_price': 10,
            'bilateral': True,
            'time_to_market': '2007-06-08',
            'trading_unit': 10,
            'deposit':0.09
        },
        "MA": {
            'type': 0,
            'commission_price': 20,
            'bilateral': True,
            'time_to_market': '2011-10-28',
            'trading_unit': 10,
            'deposit':0.08
        },
        "FG": {
            'type': 0,
            'commission_price': 30,
            'bilateral': True,
            'time_to_market': '2012-12-03',
            'trading_unit': 20,
            'deposit':0.09
        },
        "RM": {
            'type': 0,
            'commission_price': 7.5,
            'bilateral': True,
            'time_to_market': '2012-12-28',
            'trading_unit': 10,
            'deposit':0.09
        },
        "SF": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '2014-08-08',
            'trading_unit': 5,
            'deposit':0.12
        },
        "SM": {
            'type': 0,
            'commission_price': 15,
            'bilateral': False,
            'time_to_market': '2014-08-08',
            'trading_unit': 5,
            'deposit':0.12
        },
        "ZC": {
            'type': 0,
            'commission_price': 750,
            'bilateral': True,
            'time_to_market': '2013-09-26',
            'trading_unit': 100,
            'deposit':0.50
        },
        "AP": {
            'type': 0,
            'commission_price': 62.5,
            'bilateral': True,
            'time_to_market': '2017-12-22',
            'trading_unit': 10,
            'deposit':0.10
        },
        "UR": {
            'type': 0,
            'commission_price': 25,
            'bilateral': True,
            'time_to_market': '2019-08-09',
            'trading_unit': 20,
            'deposit':0.08
        },
        "SA": {
            'type': 0,
            'commission_price': 17.5,
            'bilateral': True,
            'time_to_market': '2019-12-06',
            'trading_unit': 20,
            'deposit':0.09
        }
    }
}
