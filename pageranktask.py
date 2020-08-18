# Submitted by Prinesh Bansal

import sys
from math import log2
from operator import itemgetter
from collections import defaultdict

#
# P -> Set of all pages
# S -> Set of sink nodes, that is pages which have no outlinks.
# M -> Inlink Dictionary for all pages, M[p] - is a set of pages that link to p
# L -> Outlink Count Dictionary for all pages, L[p] - is the number of outlinks from p
# d -> Damping/teleportation factor, 
#	   it is the probability that the user will continue browsing ahead.
#	   Generally set as 0.85 
#

P = []
S = []
M = {}
L = {}
d = 0.85

#
# PR -> Pagerank Dictionary, stores the values of pagerank for each page in S
# newPR -> Dictionary that temporarily stores the updated 
#		   Pagerank values before they are written in PR
# perplexity -> Stores the perplexity values for each round of pagerank
#

PR = {}
newPR = {}
perplexity = []

#
# IL -> Inlink Count Dictionary, IL[p] - is the number of inlinks to p
# SO -> Set of all source nodes, that pages which have no inlinks
#

IL = {}
SO = []

def main():
	global PR
	global IL
	global S
	global SO
	global P

	filename = sys.argv[1]
	filename1 = sys.argv[2]
	edgefile = open(filename , 'r')
	vetricefile = open(filename1,'r')
	
	print('Generating Graphs for Pagerank Calculation...')
	generate_graph(edgefile)
	print('Computing Pagerank Values...')
	compute_pagerank()
	print('\n',end = '')
	
	#
	# Printing proportion of source pages that is the ratio of number of source nodes to all nodes
	#

	print("The proportion of source pages: ",end = "")
	print(len(SO)/len(P))
	print('\n',end = '')
	
	#
	# Printing proportion of sink pages that is the ratio of number of sink nodes to all nodes
	#

	print("The proportion of sink pages: ",end = "")
	print(len(S)/len(P))
	print('\n',end = '')

	verticelist = []
	di = {}
	
	for line in vetricefile:
		nodes = line.split()
		verticelist.append(nodes)
	di = dict(verticelist)

	#
	# Generating sorted lists of pages according to their 
	# pagerank and inlink count values, sortedPR & sortedIL
	#
	
	sortedPR = sorted(PR.items(), key = itemgetter(1), reverse = True)
	sortedIL = sorted(IL.items(), key = itemgetter(1), reverse = True)

	#
	# tracking pages with final pagerank values less than uniform, initial pagerank values 
	#
	
	track = 0
	for page in sortedPR:
		if(page[1] < (1.0/len(P))):
			track += 1

	#
	# Printing proportion of pages with pagerank less than initial pagerank values
	# that is the ratio of number of such pages to all pages
	#

	print ('The proportion of pages with pagerank less than initial pagerank values are : ' + str(track/len(P)))
	print('\n',end = '')

	#write_file = open('sorted_inlink_count.txt','w')
	#write_file = open('sorted_page_rank.txt','w')

	print('Top 50 pages sorted by their pagerank values: ')
	track = 0
	for page in sortedPR:
			#write_file.write(page[0] + '\t' + di[page[0]] + '\t' + str(page[1]) + '\n')
			if(track < 50):
				print('[Node_Id]: ' + page[0] + ', [Node_name]: ' + di[page[0]] + ', [Pagerank_value]: ' + str(page[1]))
				track += 1
	print('\n',end = '')	

	print('Top 50 pages sorted by their inlink counts: ')
	track = 0			
	for page in sortedIL:
			#write_file.write(page[0] + '\t' + di[page[0]] + '\t' + str(page[1]) + '\n')
			if(track < 50):
				print('[Node_Id]: ' + page[0] + ', [Node_name]: ' + di[page[0]] + ', [Inlink_count]: ' + str(page[1]))
				track += 1	


def generate_graph(edgefile):
	global P
	global M
	global L
	global S
	global PR
	global IL
	global SO

	test = []
	dd = defaultdict(list)
	
	for line in edgefile:
		nodes = line.split()
		test.append(nodes)
		a, b = nodes[0], nodes[1]
		P.append(a)
		P.append(b)
		dd[b].append(a)
	
	
	P = list(dict.fromkeys(P))
	M = dict(dd)

	for p in P:
		if p not in M.keys():
			M[p] = []

	for p in P:
		L[p] = 0
		IL[p] = 0

	for values in M.values():
		for value in values:
			L[value] += 1

	for key in L.keys():
		if L.get(key) == 0:
			S.append(key)

	for key in M.keys():
		IL[key] = len(M.get(key))

	for i in IL:
		if IL.get(i) == 0 :
			SO.append(i)


def compute_pagerank():
	global P
	global M
	global L
	global S
	global PR
	global newPR
	global perplexity

	N = len(P)
	for p in P:
		PR[p] = 1.0/N

	i = 0
	while not converged(i):
		sinkPR = 0
		for p in S:
			sinkPR += PR[p]
		for p in P:
			newPR[p] = (1.0 - d)/N
			newPR[p] += d*sinkPR/N
			for q in M[p]:
				newPR[p] += d*PR[q]/L[q]
		for p in P:
			PR[p] = newPR[p]
		i += 1	

def converged(i):
	global perplexity

	count = 0
	perplexity.append(calculate_perplexity(i))
	if i > 0:
		change = abs(perplexity[i] - perplexity[i-1])
		if change < 1 and count <= 4:
			count += 1
			return True
		else:
			return False
	else:
		return False

def calculate_perplexity(i):
	global PR

	H = 0
	for page in PR.keys():
		H += PR[page] * log2(1/PR[page])
	perplexity = 2**H
	return perplexity


if __name__ == '__main__':
	main()