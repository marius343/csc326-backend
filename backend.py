from crawler import crawler
import utils
import pprint

pp = pprint.PrettyPrinter(indent=1, width=100)

bot = crawler(None, "urls.txt")
bot.crawl(depth=0)

#First we run the crawler on the given URLs and the page rank algorithm
inverted_index = bot.get_inverted_index()

page_rank = bot.get_raw_page_rank()
pretty_page_rank = utils.make_pagerank_pretty(page_rank, bot.get_doc_list())
#pp.pprint(pretty_page_rank)

#The page rank and word counts need to be normalized in order to combine them
#and get the importance of each given page for each given keyword
#normalized_page_rank = utils.normalize_data(page_rank)

#normalized_inverted_index = utils.normalize_data(inverted_index)

#Sorting the inverted index URL lists based on importance and resolving the inverted index
#sorted_inverted_index = utils.sort_data(normalized_inverted_index, normalized_page_rank)

resolved_inverted_index = bot.get_resovled_inverted_index()

#Store the inverted index in a database (this is what the front-end will access)
utils.add_to_frontend_database(resolved_inverted_index)
utils.add_to_backend_database(bot.get_doc_list(), page_rank, bot.get_last_doc_id())
