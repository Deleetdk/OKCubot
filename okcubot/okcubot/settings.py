# Scrapy settings for okcubot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'okcubot'

SPIDER_MODULES = ['okcubot.spiders']
NEWSPIDER_MODULE = 'okcubot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'okcubot (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
	'okcubot.pipelines.DuplicatePipeline': 300,
	'okcubot.pipelines.AnswerSanitationPipeline': 500,
	'okcubot.pipelines.MultiTSVItemPipeline': 800
}

EXTENSIONS = {'scrapy.contrib.feedexport.FeedExporter': None}

# Log
LOG_LEVEL = 'INFO'

# Human-like
ALLOWED_DOMAINS = ["okcupid.com"]
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_IP = 1

# Schedular
DEPTH_PRIORITY = 1
