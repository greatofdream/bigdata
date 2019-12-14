import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
from time import time
from sklearn import manifold, decomposition, discriminant_analysis
if len(sys.argv)<2:
    rfmName = './Result/final_dataRFM.csv'
    rfmknName = './Result/RFMKMeansKn.csv'
    visualOption = ['tsne']
else:
    rfmName = sys.argv[1]
    rfmknName = sys.argv[2]
    visualOption = sys.argv[3]
    figDir = sys.argv[4]
rfm = pd.read_csv(rfmName)
rfm_kn = pd.read_csv(rfmknName)
X = rfm.values
y = np.array(rfm_kn['cluster'])
# tsne
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0),np.max(X, 0)
    X=(X -x_min)/(x_max - x_min)
    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1],str(y[i]), color=plt.cm.Set1(y[i]/3),
                 fontdict={'weight': 'bold', 'size': 9})
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)
if 'tsne' in visualOption:
    print("Computing t-SNE embedding")
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    X_tsne = tsne.fit_transform(X)
    plot_embedding(X_tsne, "t-SNE_embedding of RFM(time:{:.2f}".format(time()-t0))
    plt.savefig(rfmName.replace('.csv','-tsne.png'))
# tsne3
def plot3_embedding(X, title=None):
    x_min, x_max = np.min(X, 0),np.max(X, 0)
    X=(X -x_min)/(x_max - x_min)
    plt.figure()
    ax = plt.subplot(111,projection='3d')
    ax.scatter(X[:, 0], X[:, 1],X[:,2], c=[plt.cm.Set1(i/3) for i in y])
    # .view_init(elev=45, azimuth=45)
    #plt.xticks([]), plt.yticks([]), plt.zticks([])
    if title is not None:
        plt.title(title)
if 'tsne3' in visualOption:
    print("Computing t-SNE embedding")
    tsne3 = manifold.TSNE(n_components=3, init='pca', random_state=0)
    t0 = time()
    X_tsne3 = tsne3.fit_transform(X)
    plot3_embedding(X_tsne3, "t-SNE_embedding of RFM(time:{:.2f}".format(time()-t0))

if 'pca' in visualOption:
    print("Computing PCA projection")
    t0 = time()
    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
    plot_embedding(X_pca,
                 "Principal Components projection of RFM (time %.2fs)" %
                   (time() - t0))

if 'discriminant' in visualOption:
    print("Computing Linear Discriminant Analysis projection")
    X2 = X.copy()
    X2.flat[::X.shape[1] + 1] += 0.01  # Make X invertible
    t0 = time()
    X_lda = discriminant_analysis.LinearDiscriminantAnalysis(n_components=2
                                                         ).fit_transform(X2, y)
    plot_embedding(X_lda,
               "Linear Discriminant projection of RFM (time %.2fs)" %
               (time() - t0))