import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import MyfarmersItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class MyfarmersSpider(scrapy.Spider):
	name = 'myfarmers'
	start_urls = ['https://www.myfarmers.bank/resources/news']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class,"btn btn-danger")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = ""
		title = response.xpath('//h2/text() | //h1/text()').get()
		content = response.xpath('//div[@class="content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=MyfarmersItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
