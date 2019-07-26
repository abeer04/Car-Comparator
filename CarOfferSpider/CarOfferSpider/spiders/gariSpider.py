# -*- coding: utf-8 -*-
import scrapy
import re

class GarispiderSpider(scrapy.Spider):
    name = 'gariSpider'
    allowed_domains = ['www.gari.pk']
    words=['honda','2020']
    start_urls = ['http://www.gari.pk/used-cars-search']
    # words=[]
    # start_urls=[]
    lua_script = """function find_search_input(inputs)
  if #inputs == 1 then
    return inputs[1]
  else
    for _, input in ipairs(inputs) do
      if input.node.attributes.type == "search" then
        return input
      end
    end
  end
end

function find_input(forms)
  local potential = {}

  for _, form in ipairs(forms) do
    local inputs = form.node:querySelectorAll('input:not([type="hidden"])')
    if #inputs ~= 0 then
      local input = find_search_input(inputs)
      if input then
        return form, input
      end

      potential[#potential + 1] = {input=inputs[1], form=form}
    end
  end

  return potential[1].form, potential[1].input
end

function main(splash, args)
  -- find a form and submit "splash" to it
  local function search_for_splash()
    local forms = splash:select_all('form')

    if #forms == 0 then
      error('no search form is found')
    end

    local form, input = find_input(forms)

    if not input then
      error('no search form is found')
    end

    assert(input:send_keys('honda'))
    assert(splash:wait(0))
    assert(form:submit())
  end

  -- main rendering script
  assert(splash:go(args.url))
  assert(splash:wait(1))
  search_for_splash()
  assert(splash:wait(10))
  --assert(splash:runjs('search_query('', (100));'))
  local button = splash:select('a[href*="search_query"]')
  button.node:setAttribute('href', "javascript: search_query('', (10))");
  button:mouse_click()
  assert(splash:wait(15))
  
  return {html = splash:html()}
  end"""

    # def __init__(self, *args, **kwargs):
    #     """
    #     Parameters
    #     ----------
    #     words : list (The list of keywords)
    #     startUrl : str (The url of the page to scrape data from)
    #     """
    #     # We are going to pass these args from our django view.
    #     # To make everything dynamic, we need to override them inside __init__ method
    #     self.words = kwargs.get('words')
    #     self.start_urls.append(kwargs.get('startUrl'))
    #     # self.words = ['city', '2016']
    #     # self.start_urls.append("https://www.pakwheels.com/used-cars/search/-/?q=city+2016")
    #     # self.start = time()
    #     super(GarispiderSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        # data = 'search_param=cars_mini/,/c_date desc/'+" ".join(str(x) for x in self.words)+'/200'
        # print(data)
        yield SplashRequest(self.start_urls[0], callback=self.parse_cars,endpoint='execute',args={'lua_source': self.lua_script})
        # yield scrapy.Request(self.start_urls[0], self.parse_cars, meta={
        #     'splash': {
        #         'args': {'lua_source': self.lua_script, 'url':self.start_urls[0]
        #         },

        #         'endpoint': 'execute',  # optional; default is render.json
        #         # 'splash_url': '0.0.0.0:8050',      # optional; overrides SPLASH_URL
        #       }
        # })

    def parse_cars(self, response):
        # scrape URLs /html/body/div[2]/div[6]/div[3]/div[1]/div[32]/div[2]/div[1]/a
        URLs = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[1]/a')
        # scrape Title /html/body/div[2]/div[6]/div[3]/div[1]/div[32]/div[2]/div[1]/a/h3/span
        titles = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[1]/a/h3/span')
        # scrape prices /html/body/div[2]/div[6]/div[3]/div[1]/div[32]/div[2]/div[2]/div[4]
        prices = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[4]')
        # scrape Locations /html/body/div[2]/div[6]/div[3]/div[1]/div[32]/div[2]/div[2]/div[2]
        locations = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[2]')
        # scrape mileage
        mileage = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[3]')
        # scrape Model
        model = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[1]')
        # scrape fuel type /html/body/div[2]/div[6]/div[3]/div[1]/div[32]/div[2]/div[2]/div[5] /html/body/div[2]/div[6]/div[3]/div[1]/div[2]/div[2]/div[3]
        fuel_type = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[5]')
        #scrape engine /html/body/div[2]/div[6]/div[3]/div[1]/div[34]/div[2]/div[2]/div[6]
        engine = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[6]')
        # scrape transmission
        transmission = response.xpath('//div[@class="fleft block_ss"]/div[2]/div[2]/div[7]')
        # scarpe Image URLs /html/body/div[2]/div[6]/div[3]/div[1]/div[34]/div[1]/span/a/img
        images = response.xpath('//div[@class="fleft block_ss"]/div[1]/span[1]/a[1]/img')

        # list of dictionaries each representing a vehicle
        items = []

        for i in range(len(URLs)):
            item = {}
            item["url"] = self.getUrl(URLs[i]) # get URL
            item["title"] = self.getTitle(titles[i]) # get title
            item["price"] = self.getPrice(prices[i]) # get price
            item["location"] = self.getLocation(locations[i]) # get location
            item["modelDate"] = self.getModel(model[i]) # get model year
            item["mileage"] = self.getMileage(mileage[i]) # get mileage
            item["fuelType"] = self.getFuel(fuel_type[i]) # get fuel type
            item["engine"] = self.getEngine(engine[i]) # get engine
            item["transmission"] = self.getTransmission(transmission[i]) # get transmission
            item["images"] = self.getImages(images[i]) # get image URLs
            items.append(item)
            # yield item

        print(items)

        # write data in a file to view the data scraped
        with open('file.txt', 'w') as f:
            for item in items:
                f.write("%s\n" % item)

    def getUrl(self, item):
        # concatenating domain name with the path of the ad
        return self.allowed_domains[0] + item.xpath('@href').extract()[0]

    def getTitle(self, item):
        return item.xpath('text()').extract()[0]

    def getPrice(self, item):
        try:
            temp = item.xpath('text()').extract()[0]
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            temp = temp.replace("Rs", "")
            temp = temp.replace("Lacs", "")
            temp = int(temp)*100000

            return temp
        except:
            return "Error at price"

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
            temp = temp.replace(" ", "")
            temp = temp.replace("\n", "")
            return temp
        except:
            return "Error at price"

    def getImages(self, item):
        return item.xpath('@src').extract()

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
