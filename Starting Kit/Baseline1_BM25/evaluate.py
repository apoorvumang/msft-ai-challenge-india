#!/usr/bin/env python
import sys, os, os.path
import numpy as np


# if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):

submission = open("answer.tsv", "r")
reference = open("../../data/reference.tsv", "r")
print("files opened")

    # submission = open("answer.tsv", "r").readlines()
    # reference = open("reference.tsv", "r").readlines()
    # assert len(submission) == len(reference), "no. of lines in submission file does not match the same in ground truth file"

preds = dict()
truths = dict()
for sub in submission:
    sub = list(map(float, sub.strip("\n").split("\t")))
    preds[int(sub[0])] = sub[1:]

for ref in reference:
    ref = list(map(int, ref.strip("\n").split("\t")))
    truths[int(ref[0])] = ref[1:]

scores = []
for q_id in truths:
    if q_id not in preds:
        scores.append(0)
    else:
        selected_psg = np.nonzero(truths[q_id])[0][0]
        # print(selected_psg)
        sorted_preds = np.argsort(preds[q_id])[::-1]
        rank = np.where(sorted_preds==selected_psg)[0][0] + 1
        scores.append(1.0/rank)

score = np.mean(scores)
print(score)

output_filename = 'scores.txt'
output_file = open(output_filename, 'w')
output_file.write("Difference: %f" % score)
output_file.close()