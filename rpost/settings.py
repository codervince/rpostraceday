# -*- coding: utf-8 -*-


BOT_NAME = 'rpost'

ITEM_PIPELINES = {
    # "rpost.pipelines.RpostPipeline":1
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

# REFERER_ENABLED = True
# COOKIES_ENABLED = True
# DOWNLOAD_DELAY = 0.25
# CONCURRENT_ITEMS = 100
# CONCURRENT_REQUESTS = 8
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# DOWNLOAD_TIMEOUT = 1000
# REDIRECT_MAX_METAREFRESH_DELAY = 1000


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html)"

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'vmac',
            'password': '',
            'database': 'rpraceday9'}
