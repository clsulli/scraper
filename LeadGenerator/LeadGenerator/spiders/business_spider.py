import scrapy
from string import ascii_lowercase as alphabet


class BusinessSpider(scrapy.Spider):
    name = "business"

    def start_requests(self):
        urls = [
            "https://www.yellowpages.com/search?search_terms=doctors&geo_location_terms=edwardsville%2C%20il&page=1",
            "https://www.yellowpages.com/search?search_terms=doctors&geo_location_terms=edwardsville%2C%20il&page=2",
            "https://www.yellowpages.com/search?search_terms=doctors&geo_location_terms=edwardsville%2C%20il&page=3",
            "https://www.yellowpages.com/search?search_terms=doctors&geo_location_terms=edwardsville%2C%20il&page=4"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        listings = response.selector.xpath("//div[@class='search-results organic']//div[@class='v-card']")

        for listing in listings:
            business_name = listing.xpath(".//a[@class='business-name']//text()").extract()
            business_page = listing.xpath(".//a[@class='business-name']//@href").extract()
            business_phone = listing.xpath(".//div[@itemprop='telephone']//text()").extract()
            business_website = listing.xpath(".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href").extract()
            print("BN: {}\nBP: {}\n BT: {}\n BW: {}\n\n".format(business_name, business_page, business_phone, business_website))

