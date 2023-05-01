数据库说明
---

数据库中共包含4个交易所44种交易品种，分别为：
```
AL.SHF 沪铝
AG.SHF 沪银
AU.SHF 沪金
BU.SHF 沥青
CU.SHF 沪铜
FU.SHF 燃油
HC.SHF 热卷
NI.SHF 沪镍
RU.SHF 橡胶
SP.SHF 纸浆
SN.SHF 沪锡
SS.SHF 不锈钢
ZN.SHF 沪锌
-----------
SC.INE 原油
-----------
A.DCE 豆一
B.DCE 豆二
C.DCE 玉米
CS.DCE 玉米淀粉
EB.DCE 苯乙烯
EG.DCE 乙二醇
J.DCE 焦炭
I.DCE 铁矿石
JD.DCE 鸡蛋
JM.DCE 焦煤
M.DCE 豆粕
L.DCE LLDPE/塑料
P.DCE 棕榈油
PG.DCE LPG
PP.DCE 聚丙烯
Y.DCE 豆油
V.DCE PVC
----------
AP.CZC 苹果
CF.CZC 棉花
FG.CZC 玻璃
OI.CZC 菜籽油
MA.CZC 甲醇
RM.CZC 菜籽粕
SA.CZC 纯碱
SF.CZC 硅铁
SM.CZC 锰硅
SR.CZC 白糖
TA.CZC PTA
ZC.CZC 动力煤
UR.CZC 尿素

```

- 如无特殊原因，数据起始时间为2015-01-04至2023-02-13

- EB.DCE苯乙烯数据为2019-09-26至2023-02-13

- SA.CZC纯碱数据为2019-11-29至2023-02-13

- AP.CZC苹果数据为2017-12-12至2023-02-13

### 各种品种数据存储方式
按照/database/{交易所代码}/{品种代码}.xlsx存储，主要包含一下字段的数据：

| 指标名称 | 意义 |	频率 |	单位 |
| ---- | ---- | ---- | ---- |
| active_con_settlement_price | 活跃合约结算价 | 日 | 元/吨 | 
| active_con_close | 活跃合约收盘价 | 日 | 元/吨 | 
| active_con_volume | 活跃合约成交量 | 日 | 手 | 
| amount | 期货成交额 | 日 | 万元 | 
| volume | 期货成交量 | 日 | 手 | 

### 其他数据
- /database/main_second_close.xlsx，为各品种主力次主力合约每天的收盘价
- /database/main_second_Itd.xlsx，为各品种主力次主力合约的最后交易日
- /database/warehouse.xlsx，为各品种主力合约的持仓量