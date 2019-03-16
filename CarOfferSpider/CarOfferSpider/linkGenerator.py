# This is a very basic link generator, we will have to modify it to get the correct results
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.pakWheels import PakwheelsSpiderSpider
from spiders.olxSpider import OlxspiderSpider
import time

def pakwheelsURL(query):
    prefix = 'https://www.pakwheels.com/used-cars/search/-/?q='

    words = query.split(' ')

    suffix = ''
    for i in range(len(words)):
        if i == 0:
            suffix += words[0]
        else:
            suffix += '+' + words[i]

    url = prefix + suffix

    return (words, url)

def olxURL(query):
    prefix = 'https://www.olx.com.pk/vehicles_c5/q-'

    words = query.split(' ')

    suffix = ''
    for i in range(len(words)):
        if i == 0:
            suffix += words[0]
        else:
            suffix += '-' + words[i]

    url = prefix + suffix

    return (words,url)

def gariUrl(query):
    prefix = 'http://www.gari.pk/used-cars/'

    words = query.split(' ')

    suffix = ''

# process = CrawlerProcess(get_project_settings())
keywords = 'city 2016'
res = pakwheelsURL(keywords)
resOlx = olxURL(keywords)
# 'pakwheelsSpider' is the name of one of the spiders of the project.
# process.crawl('pakwheelsSpider', res[0], res[1])
# process.start() # the script will block here until the crawling is finished


items = []
def collect_items(item, response, spider):
    items.append(item)

crawler = Crawler(PakwheelsSpiderSpider)
crawler.signals.connect(collect_items, signals.item_scraped)

crawlerOlx = Crawler(OlxspiderSpider)
crawlerOlx.signals.connect(collect_items, signals.item_scraped)

start = time.time()

process = CrawlerProcess(get_project_settings())
process.crawl(crawler, res[0], res[1])
process.crawl(crawlerOlx, resOlx[0], resOlx[1])
process.start()  # the script will block here until the crawling is finished

print("Scraping Completed In: ",time.time()-start)
# at this point, the "items" variable holds the scraped items
# write data in a file to view the data scraped
with open('file.txt', 'w') as f:
    for item in items:
        f.write("%s\n" % item)

sortedItems = sorted(items, key = lambda i: (-i["modelDate"], i["price"], i["mileage"]))

# write sorted data in a file to view the data scraped
with open('sortedFile.txt', 'w') as f:
    for item in sortedItems:
        f.write("%s\n" % item)

print("Total Time Taken after sorting and storing: ",time.time()-start)
