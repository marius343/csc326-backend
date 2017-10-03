from crawler import crawler

bot = crawler(None, "urls.txt")
bot.crawl(depth=1)

print "\n\nRESULTS:\n"

inverted_index = bot.get_inverted_index()
print inverted_index

resolved_inverted_index = bot.get_resovled_inverted_index()

print resolved_inverted_index