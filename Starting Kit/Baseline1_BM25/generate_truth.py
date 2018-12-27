# generate a truth file (reference.tsv) from an answer.tsv
# could be random or could be with accuracy 1

f = open("answer.tsv", "r")
fw = open("reference.tsv", "w")

random = 1

for line in f:
	line = line.strip()
	tokens = line.split("\t")
	id = tokens[0]
	to_write = id
	max_id = 0
	max = float(tokens[1])
	for i in range(2,11):
		if float(tokens[i]) >= max:
			max_id = i - 1
			max = float(tokens[i])

	if random == 1:
		max_id = 0
	for i in range(0,10):
		correct = "0"
		if i == max_id:
			correct = "1"
		to_write = to_write + "\t" + correct
	to_write += "\n"
	fw.write(to_write)

print("Created reference.tsv")