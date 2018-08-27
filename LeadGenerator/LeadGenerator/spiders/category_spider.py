import scrapy
from string import ascii_lowercase as alphabet


class CategorySpider(scrapy.Spider):
    name = "categories"

    def start_requests(self):
        url = "https://www.solidstratagems.com/google-my-business-categories/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
         cats = response.css("div.entry-content > table > tbody > tr > td > span::text").extract()
         with open("categories/categories.txt", "w") as f:
             for cat in cats:
                 f.write(cat + '\n')
