#!/usr/bin/python
#split data.tsv into train.tsv and valid.tsv
RATIO = 90 #percentage of train data
f = open("data/data.tsv", "r")
train = open("data/train.tsv", "w")
valid = open("data/valid.tsv", "w")
lines = f.readlines()
trainLastIndex = int((len(lines)*RATIO)/100)
lastQid = int(lines[trainLastIndex].split()[0])
j = trainLastIndex + 1
for i in range(j, len(lines)):
	qid = int(lines[i].split()[0])
	if qid == lastQid:
		trainLastIndex+= 1
	else:
		break
for i in range(0, trainLastIndex + 1):
	train.write(lines[i])
for i in range(trainLastIndex + 1, len(lines)):
	valid.write(lines[i])
