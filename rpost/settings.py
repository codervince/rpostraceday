 # -*- coding: utf-8 -*-

# Scrapy settings for rpost project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rpost'

ITEM_PIPELINES = {
    # "rpost.pipelines.RpostPipeline":1,
    "rpost.pipelines.CsvExportPipeline": 1,
    # "hkdata.pipelines.MyImagesPipeline":1,
    # "hkdata.pipelines.ByteStorePipeline":1,
    # "hkdata.pipelines.BasicPipelineRaceday":1,
    # "scrapy.contrib.pipeline.files.FilesPipeline": 5,
    # "hkdata.pipelines.MyFilesPipeline": 5,
    # "hkdata.pipelines.NewSQLAlchemyPipeline": 1
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1
    # "hkjc.pipelines.NoInRaceImagePipeLine": 20, 
}

SPIDER_MODULES = ['rpost.spiders']
NEWSPIDER_MODULE = 'rpost.spiders'

SPIDER_MIDDLEWARES = {
    'rpost.middlewares.Handle404Middleware': 543,
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html)"

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'vmac',
            'password': '',
            'database': 'rpraceday7'}
