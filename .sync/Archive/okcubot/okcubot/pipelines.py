# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# TODO: Validate data-pipeline
# TODO: Answer pipeline - translate answer in to a numeric value

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem
import csv
from collections import defaultdict
import os

class OkcubotPipeline(object):
    def process_item(self, item, spider):
        return item
class DuplicatePipeline(object):
	def __init__(self):
		self.usernames = self.get_column('user.tsv', 'd_username')
		self.ids = self.get_column('question.tsv', 'id')

	def process_item(self, item, spider):
		if type(item).__name__ == 'UserItem':
			return self.check_duplicate_user(item)

		if type(item).__name__ == 'QuestionItem':
			return self.check_duplicate_question(item)

		if type(item).__name__ == 'AnswerItem':
			return self.check_duplicate_answer(item)

		# Not a user, not a question, not an answer: skip.
		return item

	# Get the values of a column in a CSV-file
	def get_column(self, file, column):
		if not os.path.isfile(file):
			return list()

		columns = defaultdict(list)

		with open(file) as f:
		    reader = csv.DictReader(f)
		    for row in reader:
		        for (k,v) in row.items():
		            columns[k].append(v)

		return columns[column]

	def check_duplicate_user(self, item):
		if item['d_username'] in self.usernames:
			raise DropItem('Duplicate user found: %s' % item)
		else:
			self.usernames.append(item['d_username'])
			return item

	def check_duplicate_question(self, item):
		if item['id'] in self.ids:
			raise DropItem('Duplicate question found: %s' % item)
		else:
			self.ids.append(item['id'])
			return item

	def check_duplicate_answer(self, item):
		if item['author'] in self.usernames:
			raise DropItem('Duplicate answer found: %s' % item)
		else:
			return item

class AnswerSanitationPipeline(object):
	def __init__(self):
		self.questions = set()

	def process_item(self, item, spider):
		if type(item).__name__ == 'QuestionItem':
			self.questions.add(item)
			return item
		if type(item).__name__ != 'AnswerItem':
			return item

		question = self.find_question(item['question'])

		if question == None:
			return item

		if 'option_1' in question and item['answer'] == question['option_1']:
			item['answer'] = 1
		elif 'option_2' in question and item['answer'] == question['option_2']:
			item['answer'] = 2
		elif 'option_3' in question and item['answer'] == question['option_3']:
			item['answer'] = 3
		elif 'option_4' in question and item['answer'] == question['option_4']:
			item['answer'] = 4

		return item

	# Find question by ID
	def find_question(self, id):
		for question in self.questions:
			if question['id'] == id:
				return question

		# TODO: Find in files
		return None

class TsvItemExporter(CsvItemExporter):
	def __init__(self, *args, **kwargs):
		kwargs['encoding'] = 'utf-8'
		kwargs['delimiter'] = '\t'

		super(TsvItemExporter, self).__init__(*args, **kwargs)

#class TsvExportPipeline(object):
#	def __init__(self):
#		self.files = {}
#
#	@classmethod
#	def from_crawler(cls, crawler):
#		pipeline = cls()
#
#		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#
#		return pipeline
#
#	def spider_opened(self, spider):
#		file = open('%s_data.tsv' % spider.name, 'w+b')
#		self.files[spider] = file
#		self.exporter = TsvItemExporter(file)
#		self.exporter.start_exporting()
#
#	def spider_closed(self, spider):
#		self.exporter.finish_exporting()
#		file = self.files.pop(spider)
#		file.close()
#
#	def process_item(self, item, spider):
#		self.exporter.export_item(item)
#
#		return item

def item_type(item):
	return type(item).__name__.replace('Item', '').lower()

class MultiTSVItemPipeline(object):
	types = ['user', 'question', 'answer']

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()

		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

		return pipeline

	def spider_opened(self, spider):
		headers = True
		for name in self.types:
			if os.path.isfile('/tmp/' + name + '.tsv'):
				# File already exists -- don't write headers again
				headers = False
				break

		self.files = dict([ (name, open('/tmp/' + name + '.tsv', 'ab+')) for name in self.types ])
		self.exporters = dict([ (name, TsvItemExporter(self.files[name], include_headers_line=headers)) for name in self.types])
		[e.start_exporting() for e in self.exporters.values()]

	def spider_closed(self, spider):
		[e.finish_exporting() for e in self.exporters.values()]
		[f.close() for f in self.files.values()]

	def process_item(self, item, spider):
		what = item_type(item)

		if what in set(self.types):
			self.exporters[what].export_item(item)
			self.files[what].flush()
		return item