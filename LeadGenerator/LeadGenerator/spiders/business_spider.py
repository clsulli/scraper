import scrapy
from LeadGenerator.items import Listing


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

        for item in listings:
            business_name = item.xpath(".//a[@class='business-name']//text()").extract()
            business_page = item.xpath(".//a[@class='business-name']//@href").extract()
            business_phone = item.xpath(".//div[@itemprop='telephone']//text()").extract()
            business_website = item.xpath(".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href").extract()
            business_locality = item.xpath(".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='addressLocality']//text()").extract()
            business_region = item.xpath(".//div[@class='info']//div//p[@itemprop='address']//span[@itemprop='addressRegion']//text()").extract()

            business_name = ''.join(business_name).strip() if business_name else None
            business_page = 'https://www.yellowpages.com{}'.format(''.join(business_page).strip()) if business_page else None
            business_phone = ''.join(business_phone).strip() if business_phone else None
            business_website = ''.join(business_website).strip() if business_website else None
            business_location = '{}, {}'.format(''.join(business_locality).replace(',\xa0', '').strip(), ''.join(business_region).strip()) if business_locality and business_region else None

            listing = Listing(name=business_name,
                              detail_page=business_page,
                              phone=business_phone,
                              website=business_website,
                              location=business_location)

            #: Send to pipeline
            yield listing


