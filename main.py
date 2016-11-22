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
    #remove all sentence vectors with less than 2 entries
    for wordId in result.keys():
        if len(result[wordId]) == 1:
            result.pop(wordId)
    return result


t1 = clock()
query = "select i1.s_id, i1.w_id from inv_w as i1 join (select s_id from inv_w where w_id >= " + str(wordIdBoundary) + " group by s_id having count(*) >= " + str(minCountOfWords) + " limit 50) as i2 on i1.s_id = i2.s_id where i1.w_id >= " + str(wordIdBoundary) + " order by i1.s_id"
c1 = db.cursor()
c1.execute(query)
wordVectors = createWordVector(c1.fetchall())
sentenceVectors = createSentenceVector(wordVectors)
c1.close()
t2 = clock()
print(str(t2 - t1))

