#! /usr/bin/python3
import re
import matplotlib.pyplot as plt

def extractHeader(sqlFile):
   fsql = open(sqlFile)
   regexString = r"'(.*)'"
   name = []
   store = []
   for line in fsql:
      if re.search(r'\(', line):
         beginFlag = 1
      elif re.search(r'\)', line):
         beginFlag = 0
      if beginFlag ==1:
         matchObj =re.search(regexString, line)
         if matchObj:
            name.append(matchObj.group(1))
      else:
         matchObj =re.search(regexString, line)
         if matchObj:
            store.append({matchObj.group(1): name})
            name =[]
   return store
def plotPie(rfm_kn, label,title, method, clusterNum, saveDir='kernelKmeans'):
    customer_label_method = rfm_kn.groupby('cluster').agg({label: method})
    labelSizes = customer_label_method[label].to_numpy()
    #frequencyExplode = (0, 0, 0)
    labels = ['cluster{}'.format(i) for i in range(clusterNum)]
    plt.figure()
    plt.pie(labelSizes, labels = labels, autopct='%1.1f%%', shadow = False, startangle = 90)
    plt.title('{} proportion({})'.format(title,method))
    plt.savefig('{}/cluster{}{}Proportion_{}'.format(saveDir,clusterNum,title,method))
def clusterKernelKmeans(clusterNum, rfmMorecut, rfm_log_zs):
    model = KernelKMeans(n_clusters = clusterNum, max_iter=100,kernel=lambda X: pairwise.rbf_kernel(X, gamma=0.1))
    cluster_labels = model.fit_predict(rfm_log_zs)
    rfm_kn = rfmMoreCut.assign(cluster = cluster_labels)
    return rfm_kn
