import MySQLdb

import sys
from time import *
# DB connect information
host = ''
user = ''
passwd = ''
db = ''

# config
wordIdBoundary = 10000
minCountOfWords = 5

# create db connection
db = MySQLdb.connect(host = host,
                    user = user,
                    passwd = passwd,
                    db = db)

def createWordVector(col):
    from collections import defaultdict
    result = defaultdict(set)
    for row in col:
        result[row[0]].add(row[1])
    return result

def createSentenceVector(wordVectors):
    from collections import defaultdict
    result = defaultdict(set)
    for sentenceId in wordVectors.keys():
        for wordId in wordVectors[sentenceId]:
            result[wordId].add(sentenceId)
    return result

def createSentencePair(sentenceVectors):
	pair = []
	for sentences in sentenceVectors.values():
		if(len(sentences)>1):
			#print(sentences)
			dummySet = sentences.copy()
			while(1 < len(dummySet)):
				sentence1 = dummySet.pop()
				for sentence2 in dummySet:
					pair.append(str(sentence1) + ':' + str(sentence2))
	pair.sort()
	return pair

def countSentences(sentencePair):
	result = []
	minCommonWords = 5
	countCommonWords = 0
	i = 0
	currentPair = sentencePair[i]
	i = i + 1
	while(i<len(sentencePair)):
		if(currentPair == sentencePair[i]):
			countCommonWords = countCommonWords + 1
		else:
			if(countCommonWords > minCommonWords):
				result.append(currentPair)
			currentPair = sentencePair[i]
			countCommonWords = 0
		i = i + 1
	return result

def saveSentencePairs(sentencePairs, dbConn, fileName):
	cursor = dbConn.cursor();
	newFile = open(fileName, "w")
	for sentencePair in sentencePairs:
		sid1, sid2 = sentencePair.split(":")
		query1 = "select sentence from sentences where s_id = " + str(sid1)
		query2 = "select sentence from sentences where s_id = " + str(sid2)
		cursor.execute(query1)
		s1 = cursor.fetchone()
		cursor.execute(query2)
		s2 = cursor.fetchone()
		newFile.write(str(sid1) + ":\t" + str(s1) + "\n")
		newFile.write(str(sid2) + ":\t" + str(s2) + "\n")
		newFile.write("------------------\n")
	cursor.close()
	newFile.close()

def run(limit, fileName):
	print("Run with " + str(limit) + " sentences")
	t1 = clock()
	query = "SELECT distinct s1.s_id, w.w_id FROM sentences AS s1 INNER JOIN inv_w AS i ON s1.s_id = i.s_id INNER JOIN words AS w ON i.w_id = w.w_id AND w.w_id >= " + str(wordIdBoundary) + " limit " + str(limit)
	print(query)
	c1 = db.cursor()
	c1.execute(query)
	wordVectors = createWordVector(c1.fetchall())
	c1.close()
	print("Count WordVectors: "+ str(len(wordVectors)))
	sentenceVectors = createSentenceVector(wordVectors)
#	del wordVectors[:]
	print("Count sentenceVectors: "+ str(len(sentenceVectors)))
	sentencePair = createSentencePair(sentenceVectors)
#	del sentenceVectors[:]
	print("Count sentencePair: "+ str(len(sentencePair)))
	similarSentences = countSentences(sentencePair)
#	del sentencePair[:]
	print("Count similarSentences: "+ str(len(similarSentences)))
	t2 = clock()
	print(str(t2 - t1))
	saveSentencePairs(similarSentences, db, fileName)

run(1000, "1k.txt")
run(10000, "10k.txt")
run(100000, "100k.txt")
run(1000000, "1M.txt")
#run(10000000, "10M.txt")
