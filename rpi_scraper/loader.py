

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

class PlayerStatsLoader(ItemLoader):
	#default_input_processor = MapCompose()
	#default_output_processor = TakeFirst()

	shirt_number_in = MapCompose(lambda x: int(x))
	shirt_number_out = TakeFirst()


class MatchStatsLoader(ItemLoader):
	default_input_processor = MapCompose(lambda x: x.strip('%'))
	default_output_processor = TakeFirst()

	#_out = TakeFirst()