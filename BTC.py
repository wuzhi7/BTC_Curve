import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick  # 设置坐标样式的模块

# BTC的历史数据（从2019年7月3日到2020年9月1日），并对数据进行操作
df1 = pd.read_excel('BTC-USD.xlsx', usecols=['Date', 'Open']).convert_dtypes()   # 读取excle文件,并指定读取的列
df1.info()
df1.rename(columns={'Open' : 'BTC'}, inplace=True)    # 把'Open‘列名改为'BTC'
df1['Date'] = pd.to_datetime(df1['Date'])  # 把'Date'列转为时间格式
# print(df1[df1.isnull().T.any()])    # 检查有空字符穿的行，如果有空值，用`df1.iloc[398, 1] = 11246.20`对空值赋值

# EOS的历史数据（从2019年7月3日到2020年9月1日），并对数据进行操作
df2 = pd.read_excel('EOS-USD.xlsx',usecols=['Date', 'Open']).convert_dtypes()
df2.info()
df2['Date'] = pd.to_datetime(df2['Date'])
df2.rename(columns={'Open' : 'EOS'}, inplace=True)


# XIN的历史数据（从2019年7月3日到2020年9月1日），并对数据进行操作
df3 = pd.read_excel('XIN-USD.xlsx', usecols=['Date', 'Open']).convert_dtypes()
df3.info()
df2['Date'] = pd.to_datetime(df2['Date'])
df3.rename(columns={'Open' : 'XIN'}, inplace=True)

df = df1.merge(df2).merge(df3)   # 合并df1、df2、df3，形成新的数据

df['BOX'] = (df['BTC'] + df['EOS'] * 1500 + df['XIN'] * 8) / 10000  # 添加BOX一列
df['V-BTC'] = (df['BTC'] - df.iloc[0, 1]) / df.iloc[0, 1]       # 添加BTC价格变化一列
df['V-EOS'] = (df['EOS'] - df.iloc[0, 2]) / df.iloc[0, 2]        # 添加EOS价格变化一列
df['V-XIN'] = (df['XIN'] - df.iloc[0, 3]) / df.iloc[0, 3]       # 添加XIN价格变化一列
df['V-BOX'] = (df['BOX'] - df.iloc[0, 4]) / df.iloc[0, 4]        # 添加BOX价格变化一列
df['V-BTC_R'] = ((1000 / df['BTC']).expanding().sum() * df['BTC']) / ((df['BTC'].index + 1) * 1000)  - 1    # 添加定投BTC价格变化一列    
df['V-BOX_R'] = ((1000 / df['BOX']).expanding().sum() * df['BOX']) / ((df['BOX'].index + 1) * 1000) - 1     # 添加定投BOX价格变化一列    


plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']    # 设置plot可是可以识别汉语
plt.rcParams['axes.unicode_minus'] = False

sns.set(context='talk', style='whitegrid', palette='muted', rc={'figure.figsize': [20, 15]})    # 设置轴参数
sns.set_style({'font.sans-serif' : ['Hiragino Sans GB']})           # 设置字体可以显示中文
ax = sns.lineplot(x='Date', y='V-BTC', label='BTC', data=df)         # 在一个轴上绘制各条曲线
ax = sns.lineplot(x='Date', y='V-EOS', label='EOS', data=df)
ax = sns.lineplot(x='Date', y='V-XIN', label='XIN', data=df)
ax = sns.lineplot(x='Date', y='V-BOX', label='BOX', data=df)
ax = sns.lineplot(x='Date', y='V-BTC_R', label='RI BTC', data=df)
ax = sns.lineplot(x='Date', y='V-BOX_R', label='RI BOX', data=df)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))       # 把y轴的小数通过百分比显示
ax.set_title('虚拟货币增长曲线')



# df['V-BOX_R'] = df['V-BOX_R'].apply(lambda x: format(x, '.2%'))   # 可以把一列数据中的小数转化为百分比