#!/usr/bin/python
#creates query list
f = open("data/data.tsv", "r")
fw = open("data/query_list.txt", "w")
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

print str(len(data)) + ' records created.'

newData = sorted(data, key=lambda k: k['id']) 

for dp in newData:
	answer = ""
	for option in dp['options']:
		if option['label'] == 1:
			answer = option['answer']
			break
	fw.write(str(dp['id']) + '\t' + dp['query'] + '\n')
	fw.write(answer + '\n\n')
print 'Queries written to file'
