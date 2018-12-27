#!/usr/bin/python
#split data.tsv into train.tsv and valid.tsv
RATIO = 90 #percentage of train data
f = open("data/data.tsv", "r")
train = open("data/train.tsv", "w")
valid = open("data/valid.tsv", "w")

lines = f.readlines()
size = len(lines)

trainLastIndex = int((size*RATIO)/100)

lastQid = int(lines[trainLastIndex].split[0])
j = trainLastIndex + 1
for i in range(j, size):
	qid = int(lines[i].split[0])
	if qid == lastQid:
		trainLastIndex+= 1
	else:
		break

print lines[trainLastIndex]
print lines[trainLastIndex+1]
