
import MySQLdb
import MySQLdb.cursors

import sys
from time import *
# DB connection information
# DB host
host = 'localhost'
# DB user
user = 'dbuser'
# DB password
passwd = 'password'
# Name of used DB
dbName = 'deu_mixed_2011'

# config
# every word id less or equal this value will be ignored
wordIdBoundary = 87839
# size of length of every word vector
countOfWords = 5
# number of sentences to process, -1 indicates to process all sentences in export file
countOfSentences = -1

# create db connection
db = MySQLdb.connect(host = host,
                    user = user,
                    passwd = passwd,
                    db = dbName,
		    cursorclass = MySQLdb.cursors.SSCursor)

def createWordVectors(inputFile, countOfSentences):
	print("Creating word vector")
	import bisect
	import fileinput
	
	with open("wordvectors", "w") as file:
		# init vector
		vector = {"key": -1, "items": []}
		for inputLine in inputFile:
			if countOfSentences == 0:
				break
			sId, wId = eval(inputLine.replace("\n", ""))	
			# ignore top words
			if wId <= wordIdBoundary:
				continue
			if vector["key"] == -1: #first wordvector
				vector["key"] = sId
				vector["items"] = [wId]
			elif sId == vector["key"]: 
				# insert new wId in ascending order
				bisect.insort(vector["items"], wId)
				# delete the first item if length of list is greater than countOfWord
				if len(vector["items"]) > countOfWords:
					del vector["items"][0]
			else:
				if len(vector["items"]) == countOfWords:
	                                file.write(str(vector) + "\n")
				vector["key"] = sId
				vector["items"] = [wId]
				countOfSentences -= 1

def createSentenceVectors():
	print("Creating sentence vector")
	import fileinput
	with open("wordvectors", "r+") as file:
		open("sentencevectors", "w").close()		
		for line in file: 
			wordVector = eval(line.replace("\n", ""))
			# change sentencevector file in place
			sentenceVectorFile = fileinput.input(files=("sentencevectors"), inplace=True)
			for svLine in sentenceVectorFile:
				sentenceVector = eval(svLine.replace("\n", ""))
				# if sentenceVector["key"] is in wordVector["items"]
				# append new sId to sentenceVector and remove old wId from wordVector
				if sentenceVector["key"] in wordVector["items"]:
					sentenceVector["items"].append(wordVector["key"])
					wordVector["items"].remove(sentenceVector["key"])
				# write back to file
				print str(sentenceVector) + "\n", 
			sentenceVectorFile.close()
			# if every item in wordVector["items"] was found in sentenceVectorFile
			# creating new sentenceVectors is not necessary
			if len(wordVector["items"]) > 0:
				with open("sentencevectors", "a") as svFile:
					for wId in wordVector["items"]:
						svFile.write(str({"key": wId, "items": [wordVector["key"]]}) + "\n")
	os.remove("wordvectors")

def createSentencePairs():
	print("Create sentence pairs")
	with open("pairs", "w") as pairsFile, open("sentencevectors", "r") as svFile:
		for line in svFile:
			sentences = eval(line.replace("\n", ""))["items"]
			# copy current sentence vector			
			dummySet = list(sentences)
			# pair every sId with every other sId in this sentenceVector
			while(1 < len(dummySet)):
				sentence1 = dummySet.pop()
				for sentence2 in dummySet:
					# save new found pair in ascending order
					if sentence1 < sentence2:
						pairsFile.write(str(sentence1) + " " + str(sentence2) + "\n")
					else:
						pairsFile.write(str(sentence2) + " " + str(sentence1) + "\n")
	os.remove("sentencevectors")
					
def getSentences(dbConn, fileName):
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
	fileName = dbName
	# if file not exists get inverse list from database and sort file
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
		# sort export file in ascending order
		import subprocess
		import shutil
		subprocess.call(["sort", "--parallel=3", "-o", "temp", fileName])
		shutil.move("temp", fileName)
	with open(fileName, "r+") as export:
		createWordVectors(export, countOfSentences)
	createSentenceVectors()
	createSentencePairs()

