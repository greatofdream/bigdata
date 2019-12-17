dataDir=./data
ResultDir=./Result
prefixName=final_data
.PHONY: all
all: $(ResultDir)/final_dataRFM.csv $(ResultDir)/final_dataRFMKMeans.txt

$(ResultDir)/%RFM.csv: $(dataDir)/%.csv $(dataDir)/buildTableFinal.sql
	mkdir -p $(ResultDir)
	python3 src/dataClear.py $^ $@
$(ResultDir)/%RFMKMeans.txt: $(ResultDir)/%RFM.csv
	python3 src/kmeansCluster.py $^ $(ResultDir)/RFMKMeans.npy

.PHONY: kmeansResult
kmeansResult: $(ResultDir)/RFMKMeansKn.csv
$(ResultDir)/RFMKMeansKn.csv: $(ResultDir)/RFMKMeans.npy
	python3 src/kmeansGroup.py $^ 5 $(ResultDir)/$(prefixName)RFM.csv $@

.PHONY: visualization
visualization: $(ResultDir)/visualization/$(method).png
$(ResultDir)/visualization/%.png: $(ResultDir)/$(prefixName)RFM.csv $(ResultDir)/RFMKMeansKn.csv
	python3 visualization.py $^ ['tsne'] $(ResultDir)/visualization
.PHONY: changeFormat
changeFormat:
	iconv -f gbk -t utf-8 data/buildTable.sql -o data/buildTableU.sql

.DELETE_ON_ERROR:
.SECONDARY: