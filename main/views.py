from uuid import uuid4
from urllib.parse import urlparse
# from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from main.models import Keyword, Car, Image, KeywordCar
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

# generate url for pakwheels
def pakURL(query):
    prefix = 'https://www.pakwheels.com/used-cars/search/-/?q='

    words = query.split(' ')

    suffix = ''
    for i in range(len(words)):
        if i == 0:
            suffix += words[0]
        else:
            suffix += '+' + words[i]

    url = prefix + suffix

    return url

# generate url for olx
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

# generate url for gari
def gariURL():
    url='http://www.gari.pk/search-car-ajax.php'
    return url

# generate JSON response
def generateResponse(keywordItem):
    # sortedItems = sorted(items, key = lambda i: (-i["modelDate"], i["price"], i["mileage"]))
    data = []
    keyword_id = keywordItem.keyword_id
    keywordCar_set = KeywordCar.objects.filter(keyword_id=keyword_id)

    for keywordCar in keywordCar_set:
        car = Car.objects.get(car_id=keywordCar.car_id.car_id)
        image_set = Image.objects.filter(car_id=car.car_id)
        image_urls = []
        for image in image_set:
            image_urls.append(image.url)
        #did not converted some attributes to string
        data.append({'car_id': str(car.car_id),
                        'url': str(car.url),
                        'title': str(car.title),
                        'price': int(car.price),
                        'location': str(car.location),
                        'model': int(car.model),
                        'mileage': int(car.mileage),
                        'fuel': str(car.fuel),
                        'engine': str(car.engine),
                        'transmission': str(car.transmission),
                        'image': json.dumps(image_urls)})
    # sortedItems = sorted(data, key = lambda i: (i["price"], i["mileage"], -i["model"]))
    
    # for item in sortedItems:
    #     if item["price"] == 0:
    #         item["price"] = "NA"
    # jsonData = json.dumps(sortedItems)
    return data

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        keyword = request.POST.get('keyword', None) # take keyword from client. (From an input may be?)

        # if keyword is not found in POST request
        if not keyword:
            response = JsonResponse({"error": "missing arguments"})
            response.status_code = 400 # Bad request
            return response

        keywordItem = None
        flag = True
        err = None
        try:
            pakKeywordItem = Keyword.objects.filter(keyword=keyword).order_by("-expiryTime")[0]
            olxKeywordItem = Keyword.objects.filter(keyword=keyword).order_by("-expiryTime")[1]
            gariKeywordItem = Keyword.objects.filter(keyword=keyword).order_by("-expiryTime")[2]
        # Keyword not found
        except IndexError:
            flag = False
        except Exception as e:
            flag = False
            err = e

        # If keyword is already in database
        if (flag):
            pakData = generateResponse(pakKeywordItem)
            olxData = generateResponse(olxKeywordItem)
            garidata = generateResponse(gariKeywordItem)

            data = pakData + olxData + garidata
            sortedItems = sorted(data, key = lambda i: (i["price"], i["mileage"], -i["model"]))
            jsonData = json.dumps(sortedItems)
            return JsonResponse({'data': jsonData})
        # if keyword is not found or any error occurs
        else:
            # if any error occurs
            if (err):
                response = JsonResponse({"error": str(err)})
                response.status_code = 404 # Not found
                return response

            # create a unique id
            unique_id_pak = str(uuid4())
            unique_id_olx = str(uuid4())
            unique_id_gari = str(uuid4())

            # get the url
            pakUrl = pakURL(keyword)
            olxUrl = olxURL(keyword)
            gariUrl = gariURL()

            # This is the custom settings for scrapy spider.
            # We can send anything we want to use it inside spiders and pipelines.
            # I mean, anything
            pakSettings = {
                'unique_id': unique_id_pak, # unique ID for each record for DB
                'words': keyword, # searched keyword
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }
            olxSettings = {
                'unique_id': unique_id_olx, # unique ID for each record for DB
                'words': keyword, # searched keyword
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'ROBOTSTXT_OBEY' : False
            }
            gariSettings = {
                'unique_id': unique_id_gari, # unique ID for each record for DB
                'words': keyword, # searched keyword
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

            # Here we schedule a new crawling task from scrapyd.
            # Notice that settings is a special argument name.
            # But we can pass other arguments, though.
            # This returns a ID which belongs and will be belong to this task
            # We are going to use that to check task's status.
            # keyword = keyword.split('')
            
            taskIdGari = scrapyd.schedule('default', 'gariSpider', settings=gariSettings, words=keyword,startUrl=gariUrl)
            taskIdOlx = scrapyd.schedule('default', 'olxSpider', settings=olxSettings, words=keyword, startUrl=olxUrl)
            taskIdPak = scrapyd.schedule('default', 'pakwheelsSpider', settings=pakSettings, words=keyword, startUrl=pakUrl)


            return JsonResponse({'task_id_pak': taskIdPak,
                                'task_id_olx': taskIdOlx,
                                'task_id_gari': taskIdGari,
                                'unique_id_pak': unique_id_pak,
                                'unique_id_olx': unique_id_olx,
                                'unique_id_gari': unique_id_gari,
                                'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We were passed these from past request above. Remember?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id_pak = request.GET.get('task_id_pak', None)
        task_id_olx = request.GET.get('task_id_olx', None)
        task_id_gari = request.GET.get('task_id_gari', None)
        unique_id_pak = request.GET.get('unique_id_pak', None)
        unique_id_olx = request.GET.get('unique_id_olx', None)
        unique_id_gari = request.GET.get('unique_id_gari', None)

        # if task_id or unique_id are not found in GET request

        if not task_id_pak or not unique_id_pak or not task_id_olx or not unique_id_olx or not task_id_gari or not unique_id_gari:
            response = JsonResponse({"error": "missing arguments"})
            response.status_code = 400 # Bad request
            return response

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        pakStatus = scrapyd.job_status('default', task_id_pak)
        olxStatus = scrapyd.job_status('default', task_id_olx)
        gariStatus = scrapyd.job_status('default', task_id_gari)


        if (pakStatus == 'finished') and (olxStatus == 'finished') and (gariStatus == 'finished'):
            try:
                # this is the unique_id that we created even before crawling started.
                keywordItemPak = Keyword.objects.get(unique_id=unique_id_pak)
                keywordItemOlx = Keyword.objects.get(unique_id=unique_id_olx)
                keywordItemGari = Keyword.objects.get(unique_id=unique_id_gari)

                jsonDataPak = generateResponse(keywordItemPak)
                jsonDataOlx = generateResponse(keywordItemOlx)
                jsonDataGari = generateResponse(keywordItemGari)


                data = jsonDataOlx+jsonDataPak+jsonDataGari
                sortedItems = sorted(data, key = lambda i: (i["price"], i["mileage"], -i["model"]))
                jsonData = json.dumps(sortedItems)
                return JsonResponse({'data': jsonData})
            except Exception as e:
                response = JsonResponse({"error": str(e)})
                response.status_code = 404 # Not found
                return response
        else:
            return JsonResponse({'status': f"olx is {olxStatus} and pakwheels is {pakStatus} and Gari is {gariStatus}"})