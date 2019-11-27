import numpy as np
import pandas as pd
import datetime as dt
import sys
import rfm

if len(sys.argv) <2:
    finName = "./data/example.csv"
else:
    finName = sys.argv[1]

sqlName = "./data/buildTableU.sql"
name = rfm.extractHeader(sqlName)
dataAll = pd.read_csv(finName, sep = '\t',names = name[0]['会员消费菜品事实表'], header = None)
filterName = ['会员编号', '消费日期', '消费时间', '菜品编号', '菜品名称', '菜品数量', '菜品单价' ]

data = pd.DataFrame(dataAll, columns = filterName, dtype = 'object')
# exclude duplicate and null
dataNodup = data.drop_duplicates()
print('duplicate quantity={}'.format(data.shape[0] - dataNodup.shape[0]))
dataNodup = dataNodup.infer_objects()
dataClear = dataNodup.dropna(how = 'any')
print('NAN quantity={}'.format(dataNodup.shape[0] - dataClear.shape[0]))

