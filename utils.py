import operator
import redis

databaseIP = "localhost"

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


def make_pagerank_pretty(page_rank, doc_list):
    pretty_page_rank = [(doc_list[k], v) for k, v in page_rank.iteritems()]

    pretty_page_rank = sorted(pretty_page_rank, key=operator.itemgetter(1))

    return pretty_page_rank

def add_to_database(invertedIndex):
    database = redis.Redis(databaseIP)
    database.flushall()


    if isinstance(invertedIndex, dict):
        for word in invertedIndex:
            for url in invertedIndex[word]:
                database.zadd(word, url[0], url[1])
    else:
        print "Error: cannot add specified data structure to database"

    return

if __name__ == "__main__":
    add_to_database("blah")