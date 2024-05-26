import scrapy
from introduction_to_scrapy.items import BookItems
from urllib.parse import urlencode
import introduction_to_scrapy.settings as settings

def get_proxy_url(url: str):
    return f'https://proxy.scrapeops.io/v1/?api_key={settings.SCRAPEOPS_API_KEY}&url={url}'


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com/"]
    sops_job_name = "scrape books to scrape"

    def start_requests(self):
        yield scrapy.Request(
            url = get_proxy_url(self.start_urls[0]),
            callback = self.parse
        )

    def parse(self, response):
        links =  response.css('article h3 a')
        links = [link.attrib['href'] for link in links]
        for i in range(len(links)):
            if not 'catalogue' in links[i]:
                links[i] = f'catalogue/{links[i]}'
        links = [f'https://books.toscrape.com/{link}' for link in links]
        requests = [scrapy.Request(url=get_proxy_url(link), callback=self.parse_book_page) for link in links]

        # Itérez sur les objets Request
        for request in requests:
            yield request


        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page = f'https://books.toscrape.com/{next_page}'
            else:
                next_page = f'https://books.toscrape.com/catalogue/{next_page}'
            yield scrapy.Request(url = get_proxy_url(next_page), callback=self.parse)

    def parse_book_page(self, response):
        book_items = BookItems()
        book_items['title'] =  response.css('div.product_main h1::text').get()
        book_items['price'] =  response.css('div.product_main p.price_color::text').get()
        book_items['description'] =  response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book_items['upc'] =  response.xpath('//tr[th[contains(text(), "UPC")]]/td/text()').get()
        book_items['avaibility'] =  response.xpath('//tr[th[contains(text(), "Availability")]]/td/text()').get()

        yield book_items