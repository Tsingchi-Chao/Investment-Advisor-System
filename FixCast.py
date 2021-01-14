import pandas as pd
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rc("font",family='YouYuan')

class FixCast_Calculator:
    """FixCast_Calculator
    画出定投净值曲线，同时计算出IRR
    """

    def __init__(self,df:pd.DataFrame,cash:float,interval:int):
        """
        :param df: index为时间，column为"net_value"的dataframe,基金的净值数据
        :param cash:每次定投的金额
        :param interval:定投与定投之间的时间间隔
        """
        self.df=df
        self.cash=cash
        self.interval=interval

    def getData(self):
        """
        :return:得到总投资金额和账户累积总资产的dataframe
        """
        data = self.df.copy()
        data.loc[data.index[0], 'money'] = 0  # 此处money即客户的账户资金,初始化为0
        data.loc[data.index[0], 'investment'] = 0  # 此处investment为客户投资金额，初始化为0
        for day in range(0, len(data), self.interval):
            start_date = self.df.index[day]  # 每一个阶段的第一天定投
            data.loc[start_date, 'money'] = data.loc[start_date, 'money'] + self.cash
            data.loc[start_date, 'investment'] = data.loc[start_date, 'investment'] + self.cash
            data[day:day + self.interval + 1]['money'] = data[day:day + self.interval + 1]['net_value'] * (
                    data.loc[start_date, 'money'] / data.loc[start_date, 'net_value'])
            data[day:day + self.interval + 1]['investment'] = data.loc[start_date, 'investment']
        return data


    def drawPicture(self):
        """
        :return:画出净值曲线图，并以pdf的形式保存到当前路径下
        """
        data=FixCast_Calculator.getData(self)
        #画图
        plt.figure(dpi=200, figsize=(12, 8))
        plt.plot(data['money'],label='账户累积总资产')
        plt.plot(data['investment'],label='总投入额')

        plt.title('定投金额'+str(self.cash)+' 定投间隔时间'+str(self.interval)+'天')
        plt.legend()
        plt.savefig(r"./定投曲线.png")



    def IRR(self):
        """
        :return: 得到年化的IRR
        """
        data = FixCast_Calculator.getData(self)
        data['cash_flow']=0
        for day in range(0, len(data), self.interval):
            start_date = self.df.index[day]  # 每一个阶段的第一天定投
            data.loc[start_date,'cash_flow']=-1*self.cash
        data.loc[data.index[-1],'cash_flow']=data.loc[data.index[-1],'cash_flow']+data.loc[data.index[-1],'money']
        dailyIRR=np.irr(data['cash_flow'])
        annualIRR=(1+dailyIRR)**250-1
        return annualIRR




def main():
    data = pd.read_excel()#读取基金净值数据
    fixcast=FixCast_Calculator(data,1000,60)
    fixcast.drawPicture()
    print('年化IRR:',fixcast.IRR())

if __name__=="__main__":
    main()




