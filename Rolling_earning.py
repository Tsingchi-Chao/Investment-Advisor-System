import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rc("font",family='YouYuan')

class RollingEarning:
    """RollingEarning
    滚动计算持有固定时间的收益率分布
    """

    def __init__(self,df:pd.DataFrame,interval:int):
        """
        :param df:index为时间，column为"net_value"的dataframe,基金的净值数据
        :param interval:持有基金固定时间的间隔
        """
        self.df=df
        self.interval=interval

    def getData(self):
        """
        :return:计算得到滚动持有固定时间的收益率的dataframe，其中index为日期，columns为“net_value"和"interavalReturn"
        """
        data=self.df.copy()[['net_value']]
        data['interavalReturn']=(data['net_value'].shift(-1*self.interval)-data['net_value'])/data['net_value']
        data=data.dropna()
        return data

    def drawPicture(self):
        """
        :return:画出收益率的分布图，并讲其保存至当前路径
        """
        data=RollingEarning.getData(self)
        plt.figure(dpi=200, figsize=(12, 8))
        plt.hist(data['interavalReturn'],bins=100)
        plt.title("定投"+str(self.interval)+"天收益曲线分布")
        plt.savefig(r"./定投"+str(self.interval)+"天收益曲线分布.png")

def main():
    data=pd.read_excel()#读取数据
    rollingearning=RollingEarning(data,250)
    rollingearning.drawPicture()#画图并保存

if __name__=="__main__":
    main()



