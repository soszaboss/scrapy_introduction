import scrapy


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
        yield   {
            'Title': response.css('div.product_main h1::text').get(),
            'Price': response.css('div.product_main p.price_color::text').get(),
            'Description': response.xpath('//*[@id="content_inner"]/article/p/text()').get(),
            'UPC': response.xpath('//*[@id="content_inner"]/article/table/tbody/tr[1]/td/text()').get(),
            'Avaibility': response.xpath('//*[@id="content_inner"]/article/table/tbody/tr[6]/td/text()').get(),
            }
           