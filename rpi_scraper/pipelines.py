# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from rpi_scraper import items, settings

class RpiScraperCSVPipeline(object):

	#def __init__(self):
		#self.file = open("data.csv", 'wb')
		#self.exporter = CsvItemExporter(self.file)
		#self.exporter.start_exporting()

	def open_spider(self, spider):
		self.itemtype_to_exporter = {}
		self.files = {}

	def close_spider(self, spider):
		print((self.files))
		print(self.itemtype_to_exporter.keys())
		for exporter in self.itemtype_to_exporter.values():
			exporter.finish_exporting()
		for file in self.files.values():
			print('file closed')
			file.close()
			

	def _exporter_for_item(self, item):
		item_type = type(item).__name__
		if item_type not in self.itemtype_to_exporter:
			f = open(f"{item_type}.csv", 'wb')
			exporter = CsvItemExporter(f)
			exporter.start_exporting()
			self.itemtype_to_exporter[item_type] = exporter
			self.files[item_type] = f
		return self.itemtype_to_exporter[item_type]

	def process_item(self, item, spider):

		exporter = self._exporter_for_item(item)
		#create_valid_csv(item)
		#print((item))

		exporter.export_item(item)
		#print(f'Exported {type(item).__name__} item')
		#if isinstance(item, items.Latch):
		#	print(item)
		#	print('exporting match')
		#	self.exporter.export_item(item)
		return item


        
