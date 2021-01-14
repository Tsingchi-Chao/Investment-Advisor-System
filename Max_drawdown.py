
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

class DrawdownCalculator:
    """DrawdownCalculator
    计算最大回撤的持续期和修复期
    """

    def __init__(self,df:pd.DataFrame):
        """
        :param df:index为时间，column为"net_value"的dataframe,基金的净值数据
        """
        self.df=df

    def maxdrawdown_period(self):
        """
        :return: 最大回撤的持续期
        """
        roll_max = self.df['net_value'].expanding().max()
        end_point = np.argmin(self.df['net_value'] / roll_max - 1)
        start_point = np.argmax(self.df['net_value'][:end_point])# 找到最大回撤对应的起始index和终止index
        period=end_point-start_point
        return period

    def maxdrawdown_repair(self):
        """
        :return: 最大回撤的修复期
        """
        roll_max = self.df['net_value'].expanding().max()
        end_point = np.argmin(self.df['net_value'] / roll_max - 1)
        roll_max_value=max(self.df['net_value'][:end_point])
        data=self.df[end_point:]
        if data[data['net_value']>=roll_max_value].empty:
            print('测试期内最大回撤仍未修复')
            return;
        else:
            repair_point = self.df.index.tolist().index(data[data['net_value'] >= roll_max_value].index[0])
            repair_period=repair_point-end_point
            return repair_period


def main():
    data = pd.read_excel()#读取基金净值数据
    max_drawdown_calculator=DrawdownCalculator(data)
    print('最大回撤持续期：',max_drawdown_calculator.maxdrawdown_period())
    print('最大回撤修复期',max_drawdown_calculator.maxdrawdown_repair())

if __name__=='__main__':
    main()


