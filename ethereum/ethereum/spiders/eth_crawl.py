import scrapy
from ..items import EthereumItem


class EthCrawlSpider(scrapy.Spider):
    name = 'eth_crawl'
    # API_KEY = os.getenv("API_KEY")
    allowed_domains = ['http://www.reddit.com/']
    start_urls = ["https://www.reddit.com/r/ethereum/"]
    

    def parse(self, response):
        ethereum_item = EthereumItem()
        titles = response.css("//div[@class='y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE']/a/@href").extract()
        # votes = response.xpath("//div[@class='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo']/test()").extract()
        # comments = response.css('.FHCV02u6Cp2zYL0fhQPsO::text').getall()


