系统介绍
--- 

### 1.Config.py
该文件定义系统所需的各项参数与变量：
```
回测区间 SDate、EDate
考察区间 PeriodList，一个考察区间为Y年4月30日至Y+1年5月1日
交易所-品种 Future_Dic

各品种详情 Futures:
type： 0，按手数付费；1，按合约价值付费
bilateral：是否为双边手续费
time_to_market：何时上市
commission_price：手续费基本价格
trading_unit：每手合约交易单位
deposit：保证金比例
```

### 2.MakeTargetPool.py

**在Config.py中更新回测区间后，要更新样本池**：

```
python MakeTargetPool.py
```
样本池更新之后会将各回测区间内符合条件的交易品种更新至`/SamplePool/~`文件夹下


### 3.factor_pool.py
因子池，所有的因子定义均在此文件中

### 4.factor_weights.py
因子回测时的品种加权方式，目前实现了使用不同周期内收益率波动率序列进行加权，因每天可交易的品种数量不定，所以函数`get_volatility_df`仅返回波动率序列，在交易时根据选取的品种类型进行归一化

### 5.CBackTestEngine.py
回测引擎，进行仓位管理、可交易品种管理等。

其中的`universe_mask`是控制每天可交易品种的重要参数，是 `n(day) * m(futures)`的bool矩阵。

因子回测逻辑如下：
- trade_by_rank( )
主要用于回测`截面动量因子`、`仓单因子`和`期限结构因子`；做多因子排名前20%的品种，做空排名后20%的品种；‘equal’代表对品种等权加权，‘sort‘代表对排名归一化加权。
- trade_by_ts_rule_factor( )
主要用于回测`时序规则因子`；做多短均线大于长均线的品种，做空短均线小于长均线的品种；使用60日波动率加权。
- trade_by_ts_mome_factor( )
主要用于回测`时序动量因子`；做多因子值为正的品种，做空因子值为负的品种；使用因子值进行加权。



### 6.Logger.py
日志配置，回测时定义日志名称，回测结束后交易详情可在`/Logs/~`文件夹下面查看，回测结果在`/figs/~`文件夹下面查看

### 7.utils.py
定义了一些公用函数