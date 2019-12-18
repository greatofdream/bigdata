import numpy as np
import pandas as pd
import datetime as dt
import sys
import rfm

if len(sys.argv) <2:
    finName = "./data/example.csv"
    sqlName = "./data/buildTableU.sql"
else:
    finName = sys.argv[1]
    sqlName = sys.argv[2]
    foutName = sys.argv[3]

name = rfm.extractHeader(sqlName)
dataAll = pd.read_csv(finName, sep = '\t',names = name[0]['会员消费菜品事实表'], header = None)
filterName = ['会员编号', '消费日期', '消费时间', '菜品编号', '菜品名称', '菜品数量', '菜品单价', '会员性别','会员生日' ]
# begin clear the data
data = pd.DataFrame(dataAll, columns = filterName, dtype = 'object')
# exclude duplicate and null
dataNodup = data.drop_duplicates()
print('duplicate quantity={}'.format(data.shape[0] - dataNodup.shape[0]))
# try to infer number; maybe useless
dataNodup = dataNodup.infer_objects()
dataClear = dataNodup.dropna(how = 'any')
dataNodup.to_csv(finName.replace('.','Nodup.'), index = False)
print('NAN quantity={}'.format(dataNodup.shape[0] - dataClear.shape[0]))

# save the clear data; important: the following method is fragile
dataClear.to_csv(finName.replace('.','clear.'), index = False)

# begin analyze
dataClear['price'] = dataClear['菜品数量']*dataClear['菜品单价']
d = pd.DataFrame(dataClear, columns = ['会员编号', '消费日期', 'price'])
# sum price use person_code and date
price = d.groupby(['会员编号', '消费日期']).sum()
d = price.reset_index()

# find the recent date as the origin; caculate the frequency
date = pd.DataFrame(d,columns = ['会员编号', '消费日期'])
date = date.groupby('会员编号')
recent = date['消费日期'].max()
frequency = date['消费日期'].count()
# total price;M
pricesum = d.groupby('会员编号')['price'].sum()
# recent days;R
recentMaxDate = dt.datetime.strptime(recent.max(),'%Y-%m-%d')+dt.timedelta(days=1)
recentDays= recent.map(lambda x: (recentMaxDate - dt.datetime.strptime(x,'%Y-%m-%d')).days)
# age
age = pd.DataFrame(d,columns = ['会员编号','会员生日'])
age = age.groupby('会员编号')['会员生日'].first()
now = dt.datetime.now()
age = age.map(lambda x: int((now - dt.datetime.strptime(x,'%Y-%m-%d  %H:%M:%S')).days/356)+1)
# gender
sex=d.groupby('会员编号')['会员性别'].first()
# merge into rfm
rfm = pd.merge(pd.merge(pd.merge(pd.merge(pricesum,recentDays, on ='会员编号'),frequency,on='会员编号'), age, on='会员编号'), sex, on='会员编号')

rfm.rename(columns={'price':'money', '消费日期_x':'recent', '消费日期_y':'frequency','会员性别':'sex', '会员生日':'age'}, inplace=True)
rfm.describe()
rfm.to_csv(foutName, index = False)