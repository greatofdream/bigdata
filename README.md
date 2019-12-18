# bigdata course

author: Zhang Aiqiang

## overview

**在使用项目前需要手动建立`data`文件夹，并在其中放置对应的数据**，为避免敏感信息泄露，git项目中不提供对应的数据。

### 进展（随时更新）

+ (100%)使用jupyter完成算法和技术实现
+ (90%)使用Makefile可以运行最初的设计（包括筛选,不包括KernelKMeans算法

### 算法介绍

+ 在本项目中通过对数据进行清洗，筛选，统计，获得用户的消费信息以及其他相关信息（Recent,Frequency,Money,age,gender)。
+ 对于上述数据进行cut，去除不正确的点。对数据进行`log`操作，使得数据的大小量级一致。经测试，**归一化**操作**不需要**进行，因为会使得聚类结果变差。
+ 使用`KMeans`聚类算法，对以上的参量进行聚类，获得聚类结果。
+ 通过对于每个类别的特征分析，得出最后的优惠券发放策略。

该项目中仅包含前两部分，对于优惠券发放策略见其他分析。

## project introduction

在此之前，你需要以下的python库

+ pandas, numpy
+ matplotlib
+ impyla

### jupyter用户

项目根目录下有不同的`.ipynb`文件，为已经实现的算法，可以直接运行

+ `rfmAlpha.ipynb`为最初的实验版本，包含读入本地的`csv`数据,数据筛选，统计，得到RFM三个参量，并进行`KMeans`算法进行聚类，获得聚类结果和特征。
+ `moreFeature.ipynb`为加入了**age**,**gender**两列，和RFM三个变量共同进行`KMeans`聚类算法。
+ `moreFeaCut.ipynb`为对**R**,**F**,**M**,**age**,**gender**,中的`age`<10岁，`money`>5000限制，获得的结果。
+ `kernelKmeans.ipynb`为使用上述的cut结果，换用`KernelKMeans`算法进行聚类。
+ `impala.ipynb`中是使用**impyla**调用远程服务器的**impala**接口，对数据库进行`sql`查询.
+ `checkData.ipynb`中为检查数据格式的临时工程，可以忽略。

### vscode用户或linux命令行用户

项目中有文件夹`src`和根目录中的`Makefile`文件，执行`Make`命令即可运行`src`文件中的`.py`文件(如果你熟悉linux)。或者可以根据下面的命令手动输入，你需要注意文件名称`<>`其中的内容需要调整。如果使用`make`命令，请在`make`之前调整`Makefile`中的依赖名称。

+ python3 src/dataClear.py ./data/<final_dataRFM.csv> ./data/buildTableFinal.sql ./Result/<final_dataRFM.csv> 
+ python3 src/kmeansCluster.py ./Result/<final_dataRFM.csv> ./Result/RFMKMeans.npy
此时可以看到`Resutl`文件夹中有对应的聚类变化曲线图，选择拐点处即为最佳聚类数量，此处按照我们已有的最佳结果验证**5**输入聚类
+ python3 src/kmeansGroup.py ./Result/RFMKMeans.npy 5 ./Result/final_dataRFM.csv ./Result/RFMKMeansKn.csv
最后可以进行可视化操作，该部分**计划**使用多种可是化方法，可以在`rfmAlpha.ipynb`中找到，目前实现了`tsne`可视化，经实验验证，该种方法并不合适。

## project result

+ morefeature: 加入了 `age`,`gender`两个特征量进行聚类
+ morefeaCut: 加入了对`age`,`money`的限制，其中`age`<10岁，`money`>5000的点被剔除，因为这部分点距离较远，影响聚类效果。
+ 新进展： 去除对数据的归一化处理，聚类最后的结果更加清晰。
