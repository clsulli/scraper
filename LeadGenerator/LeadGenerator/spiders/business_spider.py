import scrapy
from LeadGenerator.items import Listing


class BusinessSpider(scrapy.Spider):
    name = "business"

    def start_requests(self):
        start_urls = create_start_urls_from_file()
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

            listing = Listing(name=business_name,
                              detail_page=business_page,
                              phone=business_phone,
                              website=business_website,
                              search_location=search_location,
                              location=business_location,
                              category=business_category)

            "https://www.yellowpages.com/search?search_terms={}&geo_location_terms=decatur%2C%20il&page={}"
            #: Send to pipeline
            yield listing


def create_start_file():
    with open('C:\\Users\\Clint\\PycharmProjects\\scraper\\LeadGenerator\\LeadGenerator\\categories\\categories3.txt', 'r') as f:
        categories = f.readlines()
        category_list = []
        for category in categories:
            category_list.append(category.strip('\n'))
        f.close()

    with open('decatur_searches.txt', 'w+') as f:
        for category in category_list:
            f.write('{} in decatur, il\n'.format(category))
        f.close()


def create_start_urls_from_file():
    with open('C:\\Users\\Clint\\PycharmProjects\\scraper\\LeadGenerator\\LeadGenerator\\categories\\categories3.txt', 'r') as f:
        categories = f.readlines()
        category_list = []
        for category in categories:
            category_list.append(category.strip('\n'))
        f.close()

    start_urls = []
    for category in category_list:
        start_urls.append("https://www.yellowpages.com/search?search_terms={}&geo_location_terms=decatur%2C%20il&page={}".format(category, 1))

    return start_urls


def lowercase():
    with open("C:\\Users\\Clint\\PycharmProjects\\scraper\\LeadGenerator\\LeadGenerator\\locations\\locations.txt", "r") as f:
        locations = []
        for location in f.readlines():
            locations.append(location.lower())
        f.close()

    with open("locations.txt", "w+") as f:
        for location in locations:
            f.write(location)
        f.close()


if __name__ == '__main__':
    lowercase()




