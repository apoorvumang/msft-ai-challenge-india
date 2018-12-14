#!/usr/bin/python
#parses the data file and prints the first and last queries
f = open("data/data.tsv", "r")
n = 0
data = []
previousQueryId = 0
query = {}
options = []
for line in f:
	line = line.strip()
	splitLine = line.split('\t')
	queryId = int(splitLine[0])
	if previousQueryId != queryId:
		if previousQueryId != 0:
			query['options'] = options
			data.append(query)
		previousQueryId = queryId
		options = []
		query = {}
		query['id'] = queryId
		query['query'] = splitLine[1].strip()	
	option = {}
	option['answer'] = splitLine[2].strip()
	option['label'] = int(splitLine[3])
	option['id'] = int(splitLine[4])
	options.append(option)
query['options'] = options
data.append(query)
print 'Number of queries = ' + str(len(data))
print data[0]
print data[len(data) - 1]
