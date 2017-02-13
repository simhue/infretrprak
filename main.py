
import MySQLdb
import MySQLdb.cursors

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
                    db = db,
		    cursorclass = MySQLdb.cursors.SSCursor)

def createWordVectors(inputFile):
	print("Creating word vector")
	import bisect
	import fileinput
	#simply create new file without adding something
	open("wordvectors", "a").close()
	progress = 0
	for inputLine in inputFile:
		if progress % 1000 == 0:
			print str(progress)
		progress += 1
		sId, wId = eval(inputLine.replace("\n", ""))	
		if wId <= 87839:
			continue
		sIdAlreadyExists = False
		vector = {}
		wordVectorFile = fileinput.input(files=("wordvectors"), inplace=True)
		for wvLine in wordVectorFile:
			#apply changes to current line in wordVectorFile
			vector = eval(wvLine.replace("\n", ""))
			if vector["key"] == sId:
				sIdAlreadyExists = True
				bisect.insort(vector["items"], wId)
			# delete the first item if length of list is greater than minCountOfWords
			if len(vector["items"]) > minCountOfWords:
				del vector["items"][0]
			#write line back to file
			print str(vector) + "\n",
		wordVectorFile.close()
		# if s_id is not yet processed, append new line to file
		if not sIdAlreadyExists:
			with open("wordvectors", "a") as file:
				file.write(str({"key": sId, "items": [wId]}) + "\n")			

def createSentenceVectors():
	print("Creating sentence vector")
	from collections import defaultdict
	import fileinput
	with open("wordvectors", "r+") as file:
		open("sentencevectors", "a").close()		
		for line in file: 
			wordVector = eval(line.replace("\n", ""))
			if len(wordVector["items"]) <= 1:
				continue
			for wId in wordVector["items"]:
				sentenceVectorFile = fileinput.input(files=("sentencevectors"), inplace=True)
				wIdAlreadyExists = False
				for svLine in sentenceVectorFile:
					sentenceVector = eval(svLine.replace("\n", ""))
					if sentenceVector["key"] == wId:
						wIdAlreadyExists = True
						sentenceVector["items"].append(wordVector["key"])
					print str(sentenceVector) + "\n", 
				sentenceVectorFile.close()
				if not wIdAlreadyExists:
					with open("sentencevectors", "a") as svFile:
						svFile.write(str({"key": wId, "items": [wordVector["key"]]}) + "\n")
	os.remove("wordvectors")

def createSentencePairs():
	print("Create sentence pairs")
	import json
	pair = []
	with open("pairs", "w") as pairsFile, open("sentencevectors", "r") as svFile:
		for line in svFile:
			sentences = eval(line.replace("\n", ""))["items"]
			if len(sentences) <= 1:
				continue
			dummySet = list(sentences)
			while(1 < len(dummySet)):
				sentence1 = dummySet.pop()
				for sentence2 in dummySet:
					if sentence1 < sentence2:
						pairsFile.write(str(sentence1) + " " + str(sentence2) + "\n")
					else:
						pairsFile.write(str(sentence2) + " " + str(sentence1) + "\n")
	os.remove("sentencevectors")
					
def saveSentencePairs(dbConn, fileName):
	with open(fileName, "w") as newFile, open("sorted-counted-pairs", "r+") as pairsFile:
		for line in pairsFile:
			sid1, sid2 = line.strip().split(" ")[1:]
			query1 = "select sentence from sentences where s_id = " + str(sid1)
			query2 = "select sentence from sentences where s_id = " + str(sid2)
			cursor = dbConn.cursor()
			cursor.execute(query1)
			s1 = cursor.fetchone()
			cursor.close()
			cursor = dbConn.cursor()
			cursor.execute(query2)
			s2 = cursor.fetchone()
			cursor.close()
			newFile.write(str(sid1) + ":\t" + str(s1) + "\n")
			newFile.write(str(sid2) + ":\t" + str(s2) + "\n")
			newFile.write("------------------\n")


if __name__ == "__main__":
	import os.path
	fileName = "test.txt"
	if not os.path.isfile(fileName):
		print("Exporting s_id, w_id from inv_w...")
		query = "SELECT s_id, w_id FROM inv_w"
		c1 = db.cursor()
		c1.execute(query)
		with open(fileName, "w") as export:
			row = c1.fetchone()
			while row is not None:
				export.write(str(row) + "\n")
				row = c1.fetchone()
		c1.close()
	with open(fileName, "r+") as export:
		createWordVectors(export)
		createSentenceVectors()
		createSentencePairs()
#	saveSentencePairs(db, "sentences.txt")

