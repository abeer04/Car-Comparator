# -*- coding: utf-8 -*-
import scrapy
import io

class GarispiderSpider(scrapy.Spider):
    name = 'gariSpider'
    allowed_domains = ['www.gari.pk']
    # start_urls = ['http://www.gari.pk/search-car-ajax.php']
    start_urls = []
    words = []
#     lua_script = """function find_search_input(inputs)
#   if #inputs == 1 then
#     return inputs[1]
#   else
#     for _, input in ipairs(inputs) do
#       if input.node.attributes.type == "search" then
#         return input
#       end
#     end
#   end
# end

# function find_input(forms)
#   local potential = {}

#   for _, form in ipairs(forms) do
#     local inputs = form.node:querySelectorAll('input:not([type="hidden"])')
#     if #inputs ~= 0 then
#       local input = find_search_input(inputs)
#       if input then
#         return form, input
#       end

#       potential[#potential + 1] = {input=inputs[1], form=form}
#     end
#   end

#   return potential[1].form, potential[1].input
# end

# function main(splash, args)
#   -- find a form and submit "splash" to it
#   local function search_for_splash()
#     local forms = splash:select_all('form')

#     if #forms == 0 then
#       error('no search form is found')
#     end

#     local form, input = find_input(forms)

#     if not input then
#       error('no search form is found')
#     end

#     assert(input:send_keys('honda'))
#     assert(splash:wait(0))
#     assert(form:submit())
#   end

#   -- main rendering script
#   assert(splash:go(args.url))
#   assert(splash:wait(1))
#   search_for_splash()
#   assert(splash:wait(10))
#   --assert(splash:runjs('search_query('', (100));'))
#   local button = splash:select('a[href*="search_query"]')
#   button.node:setAttribute('href', "javascript: search_query('', (10))");
#   button:mouse_click()
#   assert(splash:wait(15))

#   return {html = splash:html()}
#   end"""

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        words : list (The list of keywords)
        startUrl : str (The url of the page to scrape data from)
        """
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.words = kwargs.get('words')
        print(self.words)
        self.start_urls.append(kwargs.get('startUrl'))
        # self.words = ['civic', '2016']

        super(GarispiderSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        # cars_mini/,/c_date desc/civic 2016/10
        # keywords=' '.join(self.words)
        keywords=self.words
        params = 'cars_mini/,/c_date desc/'+keywords+'/100'
        print(params)
        yield scrapy.FormRequest(self.start_urls[0], callback=self.parse_cars, method='POST',
                                 formdata={'search_param': params})

        # print(data)
        # yield SplashRequest(self.start_urls[0], callback=self.parse_cars,endpoint='execute',args={'lua_source': self.lua_script})
        # yield scrapy.Request(self.start_urls[0], self.parse_cars, meta={
        #     'splash': {
        #         'args': {'lua_source': self.lua_script, 'url':self.start_urls[0]
        #         },

        #         'endpoint': 'execute',  # optional; default is render.json
        #         # 'splash_url': '0.0.0.0:8050',      # optional; overrides SPLASH_URL
        #       }
        # })

    def parse_cars(self, response):

        with io.open("gari.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        # scrape URLs  //div[@class="fleft block_ss"]/div[2]/div[1]/a
        URLs = response.xpath('//div[@id="image-cat"]/span/a')
        # scrape Title //div[@class="fleft block_ss"]/div[2]/div[1]/a/h3/span
        titles = response.xpath('//div[@id="ad-title"]/a/h3/span')
        # scrape prices //div[@class="fleft block_ss"]/div[2]/div[2]/div[4]
        prices = response.xpath('//div[@id="price-cat"]/div[4]')
        # scrape Locations //div[@class="fleft block_ss"]/div[2]/div[2]/div[2]
        locations = response.xpath('//div[@id="price-cat"]/div[2]')
        # scrape mileage //div[@class="fleft block_ss"]/div[2]/div[2]/div[3]
        mileage = response.xpath('//div[@id="price-cat"]/div[3]')
        # scrape Model //div[@class="fleft block_ss"]/div[2]/div[2]/div[1]
        model = response.xpath('//div[@id="price-cat"]/div[1]')
        # scrape fuel type //div[@class="fleft block_ss"]/div[2]/div[2]/div[5]
        fuel_type = response.xpath('//div[@id="price-cat"]/div[5]')
        #scrape engine //div[@class="fleft block_ss"]/div[2]/div[2]/div[6]
        engine = response.xpath('//div[@id="price-cat"]/div[6]')
        # scrape transmission //div[@class="fleft block_ss"]/div[2]/div[2]/div[7]
        transmission = response.xpath('//div[@id="price-cat"]/div[7]')
        # scarpe Image URLs //div[@class="fleft block_ss"]/div[1]/span[1]/a[1]/img
        images = response.xpath('//div[@id="image-cat"]/span/a/img')

        # list of dictionaries each representing a vehicle
        # items = []

        for i in range(len(URLs)):
            item = {}

            # car item
            carItem = {}
            carItem["url"] = self.getUrl(URLs[i]) # get URL
            carItem["title"] = self.getTitle(titles[i]) # get title
            carItem["price"] = self.getPrice(prices[i]) # get price
            carItem["location"] = self.getLocation(locations[i]) # get location
            carItem["model"] = self.getModel(model[i]) # get model year
            carItem["mileage"] = self.getMileage(mileage[i]) # get mileage
            carItem["fuel"] = self.getFuel(fuel_type[i]) # get fuel type
            carItem["engine"] = self.getEngine(engine[i]) # get engine
            carItem["transmission"] = self.getTransmission(transmission[i]) # get transmission

            # image item
            imageItem = {}
            imageItem["url"] = self.getImages(images[i]) # get image URL

            item["carItem"] = carItem
            item["imageItem"] = imageItem
            yield item

        # print(item)

        # write data in a file to view the data scraped
        # with io.open("items.txt", "w", encoding="utf-8") as f:
        #     f.write(str(item))

    def getUrl(self, item):
        # concatenating domain name with the path of the 
        
        return item.xpath('@href').extract()[0][7:]
    def getTitle(self, item):
        return item.xpath('text()').extract()[0]

    def getPrice(self, item):
        try:
            temp = item.xpath('text()').extract()[0]
            for token in temp.split():
                try:
                    # if this succeeds, you have your (first) float
                    temp2=temp2+float(token)
                except ValueError:
                    pass  
            temp = float(temp)*100000
            return temp
        except:
            return 0

        # if ("Call" in temp):
        #     return "Call for Price"
        # else:
        #     item = item.xpath('meta[1]')
        #     return item.xpath('@content').extract()[0]

    def getLocation(self, item):
        # strip whitespace and newline
        location = item.xpath('text()').extract()[0]

        return location

    def getModel(self, item):
        return int(item.xpath('text()').extract()[0])

    def getMileage(self, item):
        temp= item.xpath('text()').extract()[0]
        temp = int(temp.replace(" km",""))
        return temp

    def getFuel(self, item):
        return item.xpath('text()').extract()[0]

    def getEngine(self, item):
        return item.xpath('text()').extract()[0]

    def getTransmission(self, item):
        try:
            temp = item.xpath('text()').extract()[0]
            # print(temp)
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            return temp
        except:
            return 0

    def getImages(self, item):
        return item.xpath('@src').extract()[0]

        # final list of images
        # images = []
        #
        # # if (divClass):
        # #     return images
        # # else:
        # #     item = item.xpath('ul')
        # #     lst = item.xpath('@data-galleryinfo').extract()[0]
        # #     # convert string representing a list to an actual list
        # #     lst = ast.literal_eval(lst)
        # #
        # #     for i in range(len(lst)):
        # #         # scrapping image urls
        # #         images.append(lst[i]["src"])
        #
        #     return images
