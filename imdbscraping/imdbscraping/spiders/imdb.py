import scrapy
from imdbscraping.items import ImdbscrapingItem

class MoviesSpider(scrapy.Spider):
    name = 'movie_top250'
    start_urls = ('https://www.imdb.com/chart/top',)

    def parse(self, response):
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        for each in links:
            next_url = "https://www.imdb.com"+each
            yield scrapy.Request(next_url, callback=self.parse_data)
    def parse_data(self, response):
        item = ImdbscrapingItem()
        item['name'] = response.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]/h1/text()').extract()
        item['rating'] = response.xpath('//div[@class="imdbRating"]/div[@class="ratingValue"]/strong/span[@itemprop="ratingValue"]/text()').extract()[0]
        item['director'] = response.xpath('//div[@class="credit_summary_item"][h4[@class="inline"][contains(text(),"Director:") or contains(text(),"Directors:")]]/a/text()').extract()
        item['genre'] = response.xpath('//div[@class="article"]/div[@class="see-more inline canwrap"][h4[@class="inline"][contains(text(),"Genres:")]]/a/text()').extract()
        item['cast'] = response.xpath('//table[@class="cast_list"]/tr[contains(@class,"odd") or contains(@class,"even")]/td[not (contains(@class,"character") or contains(@class,"primary_photo") or contains(@class,"ellipsis"))]/a/text()').extract()
        return item
