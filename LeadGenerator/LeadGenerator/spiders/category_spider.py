import scrapy
from string import ascii_lowercase as alphabet


class CategorySpider(scrapy.Spider):
    name = "categories"

    def start_requests(self):
        start_urls = [
            'https://www.superpages.com/yellowpages/c-home+&+garden/pi-493182/',
            'https://www.superpages.com/yellowpages/c-construction+&+contractors/pi-493177/',
            'https://www.superpages.com/yellowpages/c-industry+&+agriculture/pi-517428/',
            'https://www.superpages.com/yellowpages/c-travel+&+transportation/pi-493190/',
            'https://www.superpages.com/yellowpages/c-shopping/pi-493173/',
            'https://www.superpages.com/yellowpages/c-arts+&+entertainment/pi-493174/',
            'https://www.superpages.com/yellowpages/c-media+&+communications/pi-493183/',
            'https://www.superpages.com/yellowpages/c-media+&+communications/pi-493183/',
            'https://www.superpages.com/yellowpages/c-real+estate/pi-493188/',
            'https://www.superpages.com/yellowpages/c-business+&+professional+services/pi-515925/',
            'https://www.superpages.com/yellowpages/c-sports+&+recreation/pi-493196/',
            'https://www.superpages.com/yellowpages/c-legal+&+financial/pi-493179/',
            'https://www.superpages.com/yellowpages/c-education/pi-493178/',
            'https://www.superpages.com/yellowpages/c-health+&+medicine/pi-481405/',
            'https://www.superpages.com/yellowpages/c-automotive/pi-493175/',
            'https://www.superpages.com/yellowpages/c-community+&+government/pi-493181/',
            'https://www.superpages.com/yellowpages/c-food+&+dining/pi-493189/',
            'https://www.superpages.com/yellowpages/c-clothing+&+accessories/pi-494299/',
            'https://www.superpages.com/yellowpages/c-personal+care+&+services/pi-484283/'

        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cats = response.css("ul.city-columns > li > a::text").extract()
        with open('categories2.txt', 'a+') as f:
            for cat in cats:
                f.write(cat + '\n')


def filter_categories():
    with open('C:\\Users\\Clint\\PycharmProjects\\scraper\\LeadGenerator\\categories2.txt', 'r') as f:
        cats = []
        for cat in f.readlines():
            cats.append(cat.strip('\n'))
    print(len(cats))
    cats_set = list(set(cats))
    print(len(cats_set))


if __name__ == '__main__':
    filter_categories()

