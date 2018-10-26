import scrapy
from LeadGenerator.items import Listing

class Fiverr(scrapy.Spider):
    name = "fiverr"

    def start_requests(self):
        start_urls = create_start_requests()
        for url in start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['proxy'] = 'http://209.126.120.13:8080'
            request.meta['download_timeout'] = 20
            yield request

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
            business_category = response.url.split('&geo_')[0].split('=')[1].replace('%20', ' ')
            search_location = response.url.split('location_terms=')[1].split('&page=')[0].replace('%2C', ',').replace('%20', ' ')

            yield scrapy.Request(business_page, callback=self.parse_email, meta={
                'item': {
                    'name': business_name,
                    'detail_page': business_page,
                    'phone': business_phone,
                    'website': business_website,
                    'search_location': search_location,
                    'location': business_location,
                    'category': business_category
                }
            })

    def parse_email(self, response):
        EMAIL_SELECTOR = '//a[@class="email-business"]/@href'
        item = response.meta['item']
        item['email'] = response.xpath(EMAIL_SELECTOR).extract_first()
        yield item


def create_start_requests():
    category = input('CAT >> ')
    state = input('STATE >> ')

    start_urls = []
    for i in range(1, 20):
        start_urls.append('https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}'.format(category, state, i))
    return start_urls
