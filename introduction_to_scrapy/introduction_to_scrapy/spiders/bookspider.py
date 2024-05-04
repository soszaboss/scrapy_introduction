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
        book_items['title'] =  response.css('div.product_main h1::text')[0].get(),
        book_items['price'] =  response.css('div.product_main p.price_color::text')[0].get(),
        book_items['description'] =  response.xpath('//*[@id="content_inner"]/article/p/text()').extract_first(),
        book_items['upc'] =  response.xpath('/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[1]/td/text()').extract_first(),
        book_items['avaibility'] =  response.xpath('/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[6]/td/text()').extract_first(),

        yield book_items