import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import sys
import src.rfm
if len(sys.argv)<2:
    rfmlogName = './Result/RFMKMeans.npy'
    clusterNum = 3
    rfmName = './Result/final_dataRFM.csv'
    foutName ='./Result/RFMKMeansKn.csv'
else:
    rfmlogName = sys.argv[1]
    clusterNum = int(sys.argv[2])
    rfmName = sys.argv[3]
    foutName = sys.argv[4]

rfm = pd.read_csv(rfmName)

rfm_log_zs = np.load(rfmlogName)
model = KMeans(n_clusters = clusterNum, random_state = 1)
model.fit(rfm_log_zs)
cluster_labels = model.labels_
rfm_kn = rfm.assign(cluster = cluster_labels)
rfm_kn.to_csv(foutName)
# cluster describe
rfm_kn_describe = rfm_kn.groupby('cluster').agg({'money':['mean','count'], 'recent':'mean','frequency':'mean'}).round(2)
rfm_kn_describe.to_csv(foutName.replace('.csv', 'Describle.csv'))
# plot the picture

ax = plt.subplot(111, projection = '3d')
ax.scatter(rfm_kn.iloc[:, 0], rfm_kn.iloc[:, 1], rfm_kn.iloc[:, 2], c = cluster_labels)
ax.set_xlabel('M')
ax.set_xlim([0, 7000])
ax.set_ylabel('R')
ax.set_ylim([0, 50])
ax.set_zlabel('F')
ax.set_zlim([0, 100])
plt.savefig(rfmlogName.replace('.npy', '.png'))
# plot the pie graph
resultDir = './Result'
src.rfm.plotPie(rfm_kn, 'money', 'User', 'count',clusterNum, resultDir)
src.rfm.plotPie(rfm_kn, 'money', 'Value', 'sum', clusterNum, resultDir)
src.rfm.plotPie(rfm_kn, 'money', 'Value', 'mean', clusterNum, resultDir)
src.rfm.plotPie(rfm_kn, 'frequency', 'frequency', 'mean', clusterNum, resultDir)
src.rfm.plotPie(rfm_kn, 'recent', 'recent', 'mean', clusterNum, resultDir)
'''
# user proportion
labels = ['cluster0', 'cluster1','cluster2']
sizes = rfm_kn_describe['money']['count'].to_numpy()
explode = (0, 0.2, 0.1)
plt.figure()
plt.pie(sizes, explode = explode, labels = labels, autopct='%1.1f%%', shadow = False, startangle = 90)
plt.title('user proportion ')
plt.savefig(rfmlogName.replace('.npy', 'Userproportion.png'))
# total money of each cluster
customer_sales = rfm_kn.groupby('cluster').agg({'money': 'sum'})
valueSizes = customer_sales['money'].to_numpy()
valueExplode = (0, 0.2, 0.1)
plt.figure()
plt.pie(valueSizes, explode = valueExplode, labels = labels, autopct='%1.1f%%', shadow = False, startangle = 90)
plt.title('value proportion ')
plt.savefig(rfmlogName.replace('.npy', 'Valueproportion.png'))
'''