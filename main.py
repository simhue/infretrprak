import MySQLdb

# DB connect information
i = 0
host = sys.argv[i + 1]
user = sys.argv[i + 1]
passwd = sys.argv[i + 1]
db = sys.argv[i + 1]

# config
wordIdBoundary = 1000

# create db connection
db = MySQLdb.connect(host = host,
                    user = user,
                    passwd = passwd,
                    db = db)

cursor = db.cursor()

# get word id from db
# if word does not exist or its word id is lower than wordIdBoundary, then return None
def getWordId(word):
    query = "select w_id from words where w_id > " + str(wordIdBoundary) + " and word = '" + word + "'"
    cursor.execute(query)
    result = cursor.fetchone()
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