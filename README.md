# 投资顾问系统
## FixCast.py文件
该文件定义FixCast_Calculator类，输入基金的历史数据，每次定投金额以及定投的时间间隔（如每60个交易日定投一次），就可以画出账户累积总资产和总投入额的曲线，同时计算出年化IRR，衡量出该定投策略的收益情况。

## Max_drawdown.py文件
文件定义DrawdownCalculator类，输入基金的历史数据即可计算出该基金历史上的最大回撤持续期和最大回撤的修复期。

## Rolling_earning.py文件
文件定义RollingEarning类，输入基金历史数据以及持有基金固定时间的间隔，可以计算出滚动持有基金固定时间的收益率。

## Tracking_error_IR
文件定义GETDATA类，从wind提取基金和基金基准的数据并处理得到其每天收益率的数据。FundCalculator类则根据GETDATA类得到的基金和基准的每日收益率数据计算得到该基金的跟踪误差和信息比率。同时，在文件最后，定义了可以直接从wind提取基金跟踪误差和信息比率的函数，方便直接使用。
