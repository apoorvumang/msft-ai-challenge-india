#!/usr/bin/python
#get test.tsv from data.tsv
#last ~2% of data is used as test
RATIO = 97 #percentage of train data
f = open("data/data.tsv", "r")
test = open("data/test.tsv", "w")
test_full = open("data/test_full.tsv", "w")
truth = open("data/reference.tsv", "w")
num_items = -1

lines = f.readlines()
size = len(lines)

trainLastIndex = int((size*RATIO)/100)

lastQid = int(lines[trainLastIndex].split()[0])
j = trainLastIndex + 1
for i in range(j, size):
	qid = int(lines[i].split()[0])
	if qid == lastQid:
		trainLastIndex+= 1
	else:
		break

testFirstIndex = trainLastIndex + 1


# for test.tsv, just need to copy all lines but remove the answer
# ie the second last token

# for reference.tsv, for each query there needs to be one line
# and it should have id, followed by 10 numbers (0 or 1)
# and it should be 1 for correct answer

# making test.tsv
n = 0
for i in range(testFirstIndex, size):
	lines[i] = lines[i].strip()
	t = lines[i].split('\t')
	new_line = t[0] + '\t' + t[1] + '\t' + t[2] + '\t' + t[4] + '\n'
	test.write(new_line)
	test_full.write(lines[i] + '\n')
	n+=1
	if n == num_items*10:
		break

# making reference.tsv


data = []
previousQueryId = -1
query = {}
options = []
for i in range(testFirstIndex, size):
	line = lines[i].strip()
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

data = data[1:]
# now data contains all the queries

n=0
for q in data:
	q_id = q['id']
	truth.write(str(q_id))
	correct_answer = 0
	for option in q['options']:
		if int(option['label']) == 1:
			correct_answer = int(option['id'])
	for i in range(0, 10):
		to_write = "0"
		if i == correct_answer:
			to_write = "1"
		truth.write('\t' + to_write)
	truth.write('\n')
	n += 1
	if n == num_items:
		break

