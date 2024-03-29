import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sys

if len(sys.argv)<2:
    finName = './Result/final_dataRFM.csv'
    foutName = './Result'
else:
    finName = sys.argv[1]
    foutName = sys.argv[2]

rfm = pd.read_csv(finName)
# use more feature; cut the abnormal points
rfmMore = rfm
rfmMoreCut = rfmMore.loc[(rfmMore['money']<5000)&(rfmMore['age']>10)]
rfm = rfmMoreCut
# log to normalize
rfm_log = rfm[['money', 'recent','frequency','sex','age']].apply(np.log, axis = 1).round(2)
print(rfm.shape[0])
# rfm_log_zs = (rfm_log -rfm_log.mean())/rfm_log.std()
# warning: not use normalization, the conclusion is come from this dataset
rfm_log_zs = rfm_log 
np.save(foutName, rfm_log_zs)
# use kmeans method to caculate the loss
ks = range(1, 9)
inertias = []
for k in ks:
    kc = KMeans(n_clusters = k, random_state = 1)
    kc.fit(rfm_log_zs)
    inertias.append(kc.inertia_)
with open(finName.replace('.csv', 'KMeans.txt'),'w') as fopt:
    fopt.write(np.str(inertias))
# plot the result
f,ax = plt.subplots()
plt.plot(ks, inertias, 'g-o')
plt.xlabel('cluster number')
plt.ylabel('cluster derivation')
plt.title('derivation-cluster number')
plt.savefig(finName.replace('.csv', 'KMeans.png'))