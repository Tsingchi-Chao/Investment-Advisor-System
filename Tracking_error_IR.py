#!/usr/bin/env python
# coding: utf-8

# In[1]:


from WindPy import *
w.start()
import pandas as pd
from scipy.stats.mstats import gmean
import math


# # 提取基金数据并计算基准

# In[2]:


class GETDATA:
    """GETDATA
    从wind提取数据并进行处理得到处理后的数据
    """
    def __init__(self,dic):
        """
        Args:
            windCode:In wind, different stock, industry has different and distinct code.
            start_date(str):The date that the period starts.
            end_data(str):The date that the perioed ends.
        """
        self.windCode=dic['windCode']
        self.start_date=dic['start_date']
        self.end_date=dic['end_date']
        
    def wsd_Data(self,windCode,varible:str,Name:str)->pd.DataFrame:
        """
        Args:
            variable(str):For stock, it has close,open,high etc.
            Nmae(str):The name of the varible.
        Returns:
            pd.DataFrame
        """
        data = w.wsd(windCode, varible, self.start_date, self.end_date,"PriceAdj=F")
        df = pd.DataFrame(data.Data).T
        df.index = pd.to_datetime(data.Times)
        df.columns = [Name]
        return df
    def getFinalData(self)->pd.DataFrame:
        """
        returns:得到index为时间，column为"NetValueReturn"和"BenchmarkReturn"的dataframe
        """
        data1=GETDATA.wsd_Data(self,self.windCode,'NAV_adj',Name='NetValue')
        data1['NetValueReturn']=data1['NetValue'].pct_change()
        #benchmark
        benchmarkCode=self.windCode[:-3]+'BI.'+'WI'
        data2=GETDATA.wsd_Data(self,benchmarkCode,'close',Name='Benchmark')
        data2['BenchmarkReturn']=data2['Benchmark'].pct_change()
        data=data1.join(data2)
        data=data.dropna()[['NetValueReturn','BenchmarkReturn']]
        return data


# # 计算相关指标

# In[136]:


class FundCalculator:
    """FundCalculator
    计算基金的相关指标，这里计算跟踪误差率和信息比率
    """
    def __init__(self,df):
        """
        Args:
             df即复权之后的基金净值涨跌幅以及跟踪的基准涨跌幅，index为时间，column为"NetValueReturn"和"BenchmarkReturn"
        """
        self.df=df
    def TrackingError(self):
        """
        Returns:计算得到基金的跟踪误差
        """
        data=self.df.copy()
        data['diff']=data['NetValueReturn']-data['BenchmarkReturn']
        error=data['diff'].std()* math.sqrt(250)
        return error
        
        
    def InformationRatio(self):
        """
        Returns:计算得到基金的信息比率
        """
        data=self.df.copy()
        annualExcessReturn = gmean(data['NetValueReturn'] + 1) ** 250 - 1 - (gmean(data['BenchmarkReturn'] + 1) ** 250 - 1)
        error=FundCalculator.TrackingError(self)
        IR=annualExcessReturn/error
        return IR


# # 定义主函数

# In[145]:


def main():
    res=pd.ExcelFile(r'C:\Users\ASUS\Desktop\港股指数基金处理后.xlsx')
    data=pd.read_excel(res, sheet_name='Sheet2')
    dic_fund={}
    for i in data.index:
        dic_fund[data.loc[i,'证券代码'][0:9]]=data.loc[i,'证券简称']  #存放基金代码和基金简称的字典
    Df=pd.DataFrame()  #用来存放计算的结果
    for windCode in dic_fund.keys():
        dic={}
        dic['windCode']=windCode
        dic['start_date']='2017-01-01'
        dic['end_date']='2021-01-25'
        getdata=GETDATA(dic)
        df=getdata.getFinalData()
        label=['近三个月','近六个月','近一年','近两年','近两年半','近三年']
        days=[-60,-120,-250,-500,-625,-750]
        dic_lable=dict(zip(label,days))
        Df.loc[windCode,'基金简称']=dic_fund[windCode]
        for key in dic_lable.keys():
            if len(df)>=-1*dic_lable[key]:
                data=df[dic_lable[key]:]
                fundcalculator=FundCalculator(data)
                Df.loc[windCode,key+'年化跟踪误差']=fundcalculator.TrackingError()
                Df.loc[windCode,key+'年化信息比率']=fundcalculator.InformationRatio()
    Df.to_excel(r'D:\实习\创金合信实习\量化\基金.xlsx')


# In[146]:


if __name__=="__main__":
    main()


# # 从wind直接提取跟踪误差

# In[63]:


def get_risk_annutrackerror(windCode):
    data=w.wss(windCode,"risk_annutrackerror","startDate=20201102;endDate=20210126;period=1;returnType=1;index="+str(windCode)[:-3]+"BI.WI")
    df = pd.DataFrame(data.Data).T
    df.index = pd.to_datetime(data.Times)
    df.columns = ['近三个月年化跟踪误差']
    return df
def get_IR(windCode):
    data=w.wss(windCode,"risk_annuinforatio","startDate=20201102;endDate=20210125;period=1;returnType=1;index="+str(windCode)[:-3]+"BI.WI;"+"riskFreeRate=0")
    df = pd.DataFrame(data.Data).T
    df.index = pd.to_datetime(data.Times)
    df.columns = ['近三个月年化信息比率']
    return df


# In[64]:


get_risk_annutrackerror('005051.OF')


# In[65]:


get_IR('005051.OF')


# In[66]:


get_IR('000948.OF')


# In[ ]:




