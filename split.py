#!/usr/bin/python
#split data.tsv into train.tsv and valid.tsv
RATIO_train = 5 #percentage of train data
RATIO_valid = 5

if RATIO_valid + RATIO_train > 100:
	RATIO_valid  = 100 - RATIO_train

f = open("data/data.tsv", "r")
train = open("data/train.tsv", "w")
valid = open("data/valid.tsv", "w")
lines = f.readlines()
trainLastIndex = int((len(lines)*RATIO_train)/100)
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

validLastIndex = int((len(lines)*(RATIO_train + RATIO_valid))/100)
lastQid = int(lines[validLastIndex].split()[0])
j = validLastIndex + 1

for i in range(j, len(lines)):
	qid = int(lines[i].split()[0])
	if qid == lastQid:
		validLastIndex += 1
	else:
		break

for i in range(trainLastIndex+1, validLastIndex+1):
	valid.write(lines[i])