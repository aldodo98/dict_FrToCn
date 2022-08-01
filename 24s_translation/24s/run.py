from scrapy import cmdline

cmdline.execute('scrapy crawl RootTaskSpider -o pret-a-porter.json'.split())
