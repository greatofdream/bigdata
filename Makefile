.PHONY: all
all:

.PHONY: changeFormat
changeFormat:
	iconv -f gbk -t utf-8 data/buildTable.sql -o data/buildTableU.sql
.DELETE_ON_ERROR:
.SECONDARY: