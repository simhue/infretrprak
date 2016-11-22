import MySQLdb

import sys
from _collections_abc import Set
from time import *
# DB connect information
host = sys.argv[0]
user = sys.argv[1]
passwd = sys.argv[2]
db = sys.argv[3]

# config
wordIdBoundary = 1000
minCountOfWords = 5

# create db connection
db = MySQLdb.connect(host = host,
                    user = user,
                    passwd = passwd,
                    db = db)

# get word id from db
# if word does not exist or its word id is lower than wordIdBoundary, then return None
def getWordId(word):
    cursor = db.cursor()
    query = "select w_id from words where w_id > " + str(wordIdBoundary) + " and word = '" + word + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    if result != None:
        return result[0]
    else:
        return None

def substituteWords(sentence):
    words = sentence.split(" ")
    wordVector = []
    for word in words:
        wordId = getWordId(word)
        if wordId != None:
            wordVector.append(wordId)
    return wordVector

def createWordVector(col):
    from collections import defaultdict
    result = defaultdict(list)
    collen = len(col)
    i = 0
    for row in col:
        progress = i / collen * 100
        if i % 10 == 5:
            print("Progress-Map: " + str(progress))
        result[row[0]].append(row[1])
        i += 1
    return result

t1 = clock()
query = "select i1.s_id, i1.w_id from inv_w as i1 join (select s_id from inv_w where w_id >= " + str(wordIdBoundary) + " group by s_id having count(*) >= " + str(minCountOfWords) + ") as i2 on i1.s_id = i2.s_id where i1.w_id >= " + str(wordIdBoundary) + " order by i1.s_id"
c1 = db.cursor()
c1.execute(query)
len(createWordVector(c1.fetchall()))
c1.close()
t2 = clock()
print(str(t2 - t1))

