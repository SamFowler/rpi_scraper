

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, MapCompose

class MatchLoader(ItemLoader):
	#default_input_processor = MapCompose()
	default_output_processor = TakeFirst()