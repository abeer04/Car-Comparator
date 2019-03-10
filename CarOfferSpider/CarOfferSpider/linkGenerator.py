
# This is a very basic link generator, we will have to modify it to get the correct results
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

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

    return url

def gariUrl(query):
    prefix = 'http://www.gari.pk/used-cars/'
    
    words = query.split(' ')

    suffix = ''

process = CrawlerProcess(get_project_settings())

res = pakwheelsURL('city 2016')
# 'pakwheelsSpider' is the name of one of the spiders of the project.
process.crawl('pakwheelsSpider', res[0], res[1])
process.start() # the script will block here until the crawling is finished