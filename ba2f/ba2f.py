import random

def patternToNumber(pattern):
	if len(pattern) == 0:
		return 0
	return 4 * patternToNumber(pattern[0:-1]) + symbolToNumber(pattern[-1:])

def symbolToNumber(symbol):
	if symbol == "A":
		return 0
	if symbol == "C":
		return 1
	if symbol == "G":
		return 2
	if symbol == "T":
		return 3

def numberToPattern(x, k):
	if k == 1:
		return numberToSymbol(x)
	return numberToPattern(x // 4, k-1) + numberToSymbol(x % 4)

def numberToSymbol(x):
	if x == 0:
		return "A"
	if x == 1:
		return "C"
	if x == 2:
		return "G"
	if x == 3:
		return "T"

def profileProbable(text, k, profile):
	maxprob = 0
	kmer = text[0:k]
	for i in range(0,len(text) - k +1):
		prob = 1
		pattern = text[i:i+k]
		for j in range(k):
			l = symbolToNumber(pattern[j])
			prob *= profile[l][j]
		if prob > maxprob:
			maxprob = prob
			kmer = pattern
	return kmer

def hammingDistance(p, q):
	ham = 0
	for x, y in zip(p, q):
		if x != y:
			ham += 1
	return ham

def distanceBetweenPatternAndString(pattern, dna):
	k = len(pattern)
	distance = 0
	for x in dna:
		hamming = k+1
		for i in range(len(x) - k + 1):
			z = hammingDistance(pattern, x[i:i+k])
			if hamming > z:
				hamming = z
		distance += hamming
	return distance

def profileForm(motifs):
	k = len(motifs[0])
	profile = [[1 for i in range(k)] for j in range(4)]
	for x in motifs:
		for i in range(len(x)):
			j = symbolToNumber(x[i])
			profile[j][i] += 1
	for x in profile:
		for i in range(len(x)):
			x[i] = x[i]/len(motifs)
	return profile

def consensus(profile):
	str = ""
	for i in range(len(profile[0])):
		max = 0
		loc = 0
		for j in range(4):
			if profile[j][i] > max:
				loc = j
				max = profile[j][i]
		str+=numberToSymbol(loc)
	return str

def score(motifs):
	profile = profileForm(motifs)
	cons = consensus(profile)
	score = 0
	for x in motifs:
		for i in range(len(x)):
			if cons[i] != x[i]:
				score += 1
	return score

def randomMotifSearch(dna, k, t):
	bestMotifs = []
	motifs = []
	for x in range(t):
		random.seed()
		i = random.randint(0, len(dna[x])-k)
		motifs.append(dna[x][i:i+k])
	bestMotifs = motifs.copy()
	count = 0
	while True:
		profile = profileForm(motifs)
		for x in range(t):
			motifs[x] = profileProbable(dna[x], k, profile)
		if score(motifs) < score(bestMotifs):
			bestMotifs = motifs.copy()
			count+=1
		else:
			print(count)
			return bestMotifs

k = 8
t = 5
dna = ["CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA","GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG","TAGTACCGAGACCGAAAGAAGTATACAGGCGT","TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",""]
best = randomMotifSearch(dna, k, t)
min = score(best)
for x in range(1000):
	print(x)
	a = randomMotifSearch(dna, k, t)
	if score(a) < score(best):
		best= a
		min = score(a)
print(min)
for x in best:
	print(x)