import operator
import redis

databaseIP = "34.226.148.225"

#Normalizes data on a scale of 0 to 100 by finding max and min and adjusting accordingly
#Can take in a dictionary or a list
def normalize_data(inputData):
    if isinstance(inputData, dict):
        if len(inputData) < 2:
            return inputData
        #case for when input is page rank dictionary
        elif isinstance(inputData.values()[0], float):
            maxVal = max(inputData.iteritems(), key=operator.itemgetter(1))[1]
            minVal = min(inputData.iteritems(), key=operator.itemgetter(1))[1]

            for key in inputData:
                inputData[key] = (inputData[key] - minVal) / (maxVal - minVal) * 100

            return inputData
        #case for when input is inverted index with a list of [doc_id, word occurance counts] as the value
        elif isinstance(inputData.values()[0], list):
            for word in inputData:
                maxVal = max([sublist[-1] for sublist in inputData[word]])
                minVal = min([sublist[-1] for sublist in inputData[word]])

                for page in inputData[word]:
                    if(maxVal != minVal): page[1] = (float(page[1]) - minVal) / (maxVal - minVal) * 100
                    else: page[1] = 100

            return inputData

    else:
        print "Error: Invalid data type, cannot normalize"


    return []


#sorts the normalized data, note that if page rank is not specified, it will only sort by number of word occurences
def sort_data(inverted_index, page_rank = {}):

    if isinstance(inverted_index, dict):

        for word in inverted_index:
            #First, we need to aggragate word count and page_rank data (if possible)
            if isinstance(page_rank, dict) and len(page_rank) > 1:
                for page in inverted_index[word]:
                    page[1] = 0.5 * page[1] + 0.5* page_rank.get(page[0], 0)
                    inverted_index[word] = sorted(inverted_index[word], key=operator.itemgetter(1), reverse=True)

        return inverted_index

    else:

        print "Error: Inverted index is not a dictionary"

        return {}

#Makes the pagerank more readable when printing it
def make_pagerank_pretty(page_rank, doc_list):
    pretty_page_rank = [(doc_list[k], v) for k, v in page_rank.iteritems()]

    pretty_page_rank = sorted(pretty_page_rank, key=operator.itemgetter(1))

    return pretty_page_rank

#Adds to backend database. The backend database has DOC_IDs as the keys and the list [URL, page_rank] as the value
def add_to_backend_database(document_list, page_rank, nextDocID):
    database = redis.Redis("localhost")

    #Need this to ensure duplicate IDs are not pushed, crawler MUST load this value everytime it runs
    database.rpush("nextDocID", nextDocID)

    if isinstance(document_list, dict) and isinstance(page_rank, dict):
        for doc_id in document_list:
            database.rpush(doc_id, document_list[doc_id])
            database.rpush(doc_id, page_rank.get(doc_id, 0))
    else:
        print "Error: cannot add specified structures to frontend database"

    return


#Adds inverted index to frontend database.
#Format for database is word:ordered_set(pageID, wordCount)
def add_to_frontend_database(invertedIndex):
    database = redis.Redis(databaseIP)

    indexSize = len(invertedIndex)
    currentWordID = 0

    if isinstance(invertedIndex, dict):
        for word in invertedIndex:
            print currentWordID, "/", indexSize
            for url in invertedIndex[word]:
                database.zadd(word, url[0], url[1])
            currentWordID += 1

    else:
        print "Error: cannot add specified data structure to frontend database"

    return

if __name__ == "__main__":
    add_to_frontend_database("blah")