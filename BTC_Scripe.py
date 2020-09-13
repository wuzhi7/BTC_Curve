import requests
import pandas as pd
from pathlib import Path
import numpy as np
import os
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from bs4 import BeautifulSoup

# 设置主网页，以及各子网页的组成部分，**修改`data`中的`start`与`end`中的时间，可以自定义要分析哪些数据
BASE_ULR = 'https://coinmarketcap.com/currencies/'  # 主网址
# category = ['bitcoin', 'eos', 'mixin']
con = '/historical-data/?'     # 网址中间固定的部分
date = 'start=20190101&end=20200911'   # **修改`data`中的`start`与`end`中的时间，可以自定义要分析哪些数据


# 定义一个抓取网页数据成为表格的函数
def grab_data_from_html(cur) -> pd.DataFrame:
    page = BASE_ULR + cur + con + date  # 页面网址

    response = requests.get(page)
    if response.status_code == 200:  #  确保能够读取这个网页
        soup = BeautifulSoup(response.content, 'html.parser')  # 用beautiful解析页面 'html.parser' 为网页解析器
        # 找到表格th数据
        table = soup.find('span', string='Currency in USD').parent.find_next_sibling('div').find('table')
        column_names = [th.text for th in table.thead.tr.find_all('th')]  # 定义表格列名
        # 找到表格td数据
        table1 = soup.find('span', string='Currency in USD').parent.find_next_sibling('div').find('tbody')
        data_rows = []
        for tr in table1.find_all('tr'):    # 找到所有行
            row = [td.text for td in tr.find_all('td')]
            data_rows.append(row)

    df = pd.DataFrame(data_rows, columns=column_names)   # 创建DataFrame

    return df


# 显示这一部分代码，可以生成data_out中的数据
# if __name__ == '__main__':     
#     df_xin = grab_data_from_html('mixin')
#     df_xin.to_excel('/Users/liyangbin/BTC_value/data_out/XIN.xlsx', index=False)
#     df_eos = grab_data_from_html('eos')
#     df_eos.to_excel('/Users/liyangbin/BTC_value/data_out/EOS.xlsx', index=False)
#     df_btc = grab_data_from_html('bitcoin')
#     df_btc.to_excel('/Users/liyangbin/BTC_value/data_out/BTC.xlsx', index=False)



# 整理表格数据
def merge_data(folder) -> pd.DataFrame:

    df_list = []
    for fn in os.listdir(folder):  # 遍历一个文件夹中的所有文件
        afn = os.path.join(folder, fn)  # 定义一个绝对路径 
       
        df_temp = pd.read_excel(afn, usecols=['Date', 'Open*'], index_col=[0])  # 读取每一个Excel文件,并选取指定的列
        df_temp = df_temp.rename(columns={'Open*' : fn.split('.')[0]}) # 对列进行重命名
        df_list.append(df_temp)  # 把每一个读取的文件添加到空的列表中
        
    df = pd.concat(df_list, axis=1) # 合并3个表格

   
    return df
    

if __name__ == '__main__':   
    df = merge_data('/Users/liyangbin/project/data_out')
    df.to_excel('/Users/liyangbin/BTC_value/all_out/BTC_XIN_EOS.xlsx')


# 生成最终的表格
df = pd.read_excel('/Users/liyangbin/BTC_value/all_out/BTC_XIN_EOS.xlsx', thousands=",").convert_dtypes()
df = df.sort_index(ascending=False, ignore_index=True)   #改为降序
df['Date'] = pd.to_datetime(df['Date'])

# df['BTC'] = pd.to_numeric(df['BTC'], errors='coerce')
df.dtypes

df['BOX'] = (df['BTC'] + df['EOS'] * 1500 + df['XIN'] * 8) / 10000
df['V-BTC'] = (df['BTC'] - df.iloc[0, 1]) / df.iloc[0, 1]
df['V-EOS'] = (df['EOS'] - df.iloc[0, 3]) / df.iloc[0, 3]
df['V-XIN'] = (df['XIN'] - df.iloc[0, 2]) / df.iloc[0, 2]
df['V-BOX'] = (df['BOX'] - df.iloc[0, 4]) / df.iloc[0, 4]
df['V-BTC_RI'] = ((1000 / df['BTC']).expanding().sum() * df['BTC']) / ((df['BTC'].index + 1) * 1000)  - 1
df['V-BOX_RI'] = ((1000 / df['BOX']).expanding().sum() * df['BOX']) / ((df['BOX'].index + 1) * 1000) - 1
df['V-BTC'] = df['V-BTC'].apply(lambda x: format(x, '.2%'))
df['V-EOS'] = df['V-EOS'].apply(lambda x: format(x, '.2%'))
df['V-XIN'] = df['V-XIN'].apply(lambda x: format(x, '.2%'))
df['V-BOX'] = df['V-BOX'].apply(lambda x: format(x, '.2%'))
df['V-BTC_RI'] = df['V-BTC_RI'].apply(lambda x: format(x, '.2%'))
df['V-BOX_RI'] = df['V-BOX_RI'].apply(lambda x: format(x, '.2%'))
df.to_excel('/Users/liyangbin/BTC_value/all_out/V-BTC_XIN_EOS_BOX.xlsx')
df

# 展示数据
df['BOX'] = (df['BTC'] + df['EOS'] * 1500 + df['XIN'] * 8) / 10000
df['V-BTC'] = (df['BTC'] - df.iloc[0, 1]) / df.iloc[0, 1]
df['V-EOS'] = (df['EOS'] - df.iloc[0, 3]) / df.iloc[0, 3]
df['V-XIN'] = (df['XIN'] - df.iloc[0, 2]) / df.iloc[0, 2]
df['V-BOX'] = (df['BOX'] - df.iloc[0, 4]) / df.iloc[0, 4]
df['V-BTC_RI'] = ((1000 / df['BTC']).expanding().sum() * df['BTC']) / ((df['BTC'].index + 1) * 1000)  - 1
df['V-BOX_RI'] = ((1000 / df['BOX']).expanding().sum() * df['BOX']) / ((df['BOX'].index + 1) * 1000) - 1


sns.set(context='talk', style='whitegrid', palette='muted', rc={'figure.figsize': [30, 20], 'font.sans-serif' : ['Hiragino Sans GB']})
ax = sns.lineplot(x='Date', y='V-BTC', label='BTC', data=df)
ax = sns.lineplot(x='Date', y='V-EOS', label='EOS', data=df)
ax = sns.lineplot(x='Date', y='V-XIN', label='XIN', data=df)
ax = sns.lineplot(x='Date', y='V-BOX', label='BOX', data=df)
ax = sns.lineplot(x='Date', y='V-BTC_RI', label='RI BTC', data=df)
ax = sns.lineplot(x='Date', y='V-BOX_RI', label='RI BOX', data=df)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_title('虚拟货币增长曲线' )
ax.set_ylabel('增长率')
ax.set_xlabel('时间')
fig = ax.get_figure()
plt.savefig('/Users/liyangbin/BTC_value/all_out/BTC_Value.jpg', dpi=150)