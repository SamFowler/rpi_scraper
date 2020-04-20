
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, MapCompose

class SeasonLoader(ItemLoader):
	default_input_processor = MapCompose()