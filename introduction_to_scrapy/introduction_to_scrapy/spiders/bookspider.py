import scrapy
from introduction_to_scrapy.items import BookItems

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        links =  response.css('article h3 a')
        yield from response.follow_all(links, callback=self.parse_book_page)
        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_book_page(self, response):
        book_items = BookItems()
        book_items['title'] =  response.css('div.product_main h1::text').get()
        book_items['price'] =  response.css('div.product_main p.price_color::text').get()
        book_items['description'] =  response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book_items['upc'] =  response.xpath('//tr[th[contains(text(), "UPC")]]/td/text()').get()
        book_items['avaibility'] =  response.xpath('//tr[th[contains(text(), "Availability")]]/td/text()').get()

        yield book_items