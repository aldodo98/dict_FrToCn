import scrapy
from scrapy.http import Request
import random
from datetime import datetime
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
spackage = __import__('items')
import json
import re
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars




class RoottaskspiderSpider(scrapy.Spider):
    name = 'RootTaskSpider'
    allowed_domains = ['https://www.24s.com']
    main_url = '24s.com/'
    fr_urls = 'https://api.zolaprod.babylone.io/proxy-search/algolia/products?index=zolaprod_products&country=FR&locale=fr&date=2022-07-21T10:02:34.609Z&queries=%7B%22tagFilters%22:[%22FR%22,%22women_rtw%22,%22women_rtw%22,%22women%22],%22disjunctiveFacets%22:%7B%22brand%22:[],%22color_fr_pack%22:[],%22clothing_size_FR%22:[],%22clothing_size_US%22:[],%22clothing_size_UK%22:[],%22clothing_size_IT%22:[],%22clothing_size_DE%22:[],%22clothing_size_JP%22:[],%22shoes_size_EU%22:[],%22shoes_size_FR%22:[],%22shoes_size_US%22:[],%22shoes_size_UK%22:[],%22shoes_size_JP%22:[],%22shoes_size_KOR%22:[],%22promotion_event_type%22:[]%7D,%22hierarchicalFacets%22:[],%22numericFilters%22:[[%22discontinued%22,%22%3D%22,0]],%22page%22:8,%22refine%22:%22%22,%22searchType%22:%22category%22,%22hierarchy%22:%22hierarchy_fr%22,%22facetsToExclude%22:%7B%22brand%22:[]%7D,%22ruleContexts%22:[%22women_rtw_COUNTRY_FR%22],%22hitsPromotedInPage%22:[%22DIO22Z561998-or%22,%22CELYZJW8off-white%22,%22ZIMSVD25bouquet-floral%22,%22ZIM82M5Ypatch-paisley%22,%22LDJ73B86lily%22,%22JACJHRK5yellow%22,%22LVUK5SU9rouge%22,%22EREFUV9Elimonade%22,%22ZIM3GTP7mustard%22,%22FARM54Y4flower-dream%22,%22EIM755ZWraspberry%22,%22ZIMGE98Zred-palm%22,%22LOE7EE88white-multicolor%22,%22FENUR52Qnoir%22,%22CEL8H9Q5black%22,%22DIO8244G1998-or%22,%22ZIMCN74Qivory%22,%22ZIMCKG52spliced%22,%22CELBT326black%22,%22DIO67PTE1700-beige%22,%22LOEF38Q5ecru%22,%22CELQ8494dark-union-wash%22,%22FARP8732off-white%22,%22CHLKT8N4off-brown%22,%22AMQ554AGblack%22,%22VAL4ANK6z42%22,%22LDJ56ZRHbianco%22,%22MAXNY277cammello%22,%22LOEWRXZ4indigo-blue%22,%22ZIMX9948red-palm%22,%22GIV66ST3blanc%22,%22MAXKSDMGcammello%22,%22APCB3A6Nblue%22,%22CHLNF753white-powder%22,%22ROT94GKAegret%22,%22ZIM4A945floral-swirl%22,%22ZIMVM68Ffloral-swirl%22,%22CUCVHAS3lessive%22,%22BLM82N95rouge%22,%22EREX3ZMXcactus%22,%22MUS46494ecru%22,%22MAXZ8HM3cammello%22,%22BASE3YXCgreen%22],%22preview%22:%22%22,%22hitsPerPage%22:1000,%22analyticsTags%22:[%22platform:frontend%22,%22type:products%22,%22page:plp%22,%22lang:FR%22,%22country:fr%22]%7D'
    cn_urls = ['https://api.zolaprod.babylone.io/proxy-search/algolia/products?index=zolaprod_products&country=FR&locale=zh&date=2022-07-21T10:02:06.411Z&queries=%7B%22tagFilters%22:[%22FR%22,%22women_rtw%22,%22women_rtw%22,%22women%22],%22disjunctiveFacets%22:%7B%22brand%22:[],%22color_zh_pack%22:[],%22clothing_size_FR%22:[],%22clothing_size_US%22:[],%22clothing_size_UK%22:[],%22clothing_size_IT%22:[],%22clothing_size_DE%22:[],%22clothing_size_JP%22:[],%22shoes_size_EU%22:[],%22shoes_size_FR%22:[],%22shoes_size_US%22:[],%22shoes_size_UK%22:[],%22shoes_size_JP%22:[],%22shoes_size_KOR%22:[],%22promotion_event_type%22:[]%7D,%22hierarchicalFacets%22:[],%22numericFilters%22:[[%22discontinued%22,%22%3D%22,0]],%22page%22:8,%22refine%22:%22%22,%22searchType%22:%22category%22,%22hierarchy%22:%22hierarchy_zh%22,%22facetsToExclude%22:%7B%22brand%22:[]%7D,%22ruleContexts%22:[%22women_rtw_COUNTRY_FR%22],%22hitsPromotedInPage%22:[%22DIO22Z561998-or%22,%22CELYZJW8off-white%22,%22ZIMSVD25bouquet-floral%22,%22ZIM82M5Ypatch-paisley%22,%22LDJ73B86lily%22,%22JACJHRK5yellow%22,%22LVUK5SU9rouge%22,%22EREFUV9Elimonade%22,%22ZIM3GTP7mustard%22,%22FARM54Y4flower-dream%22,%22EIM755ZWraspberry%22,%22ZIMGE98Zred-palm%22,%22LOE7EE88white-multicolor%22,%22FENUR52Qnoir%22,%22CEL8H9Q5black%22,%22DIO8244G1998-or%22,%22ZIMCN74Qivory%22,%22ZIMCKG52spliced%22,%22CELBT326black%22,%22DIO67PTE1700-beige%22,%22LOEF38Q5ecru%22,%22CELQ8494dark-union-wash%22,%22FARP8732off-white%22,%22CHLKT8N4off-brown%22,%22AMQ554AGblack%22,%22VAL4ANK6z42%22,%22LDJ56ZRHbianco%22,%22MAXNY277cammello%22,%22LOEWRXZ4indigo-blue%22,%22ZIMX9948red-palm%22,%22GIV66ST3blanc%22,%22MAXKSDMGcammello%22,%22APCB3A6Nblue%22,%22CHLNF753white-powder%22,%22ROT94GKAegret%22,%22ZIM4A945floral-swirl%22,%22ZIMVM68Ffloral-swirl%22,%22CUCVHAS3lessive%22,%22BLM82N95rouge%22,%22EREX3ZMXcactus%22,%22MUS46494ecru%22,%22MAXZ8HM3cammello%22,%22BASE3YXCgreen%22],%22preview%22:%22%22,%22hitsPerPage%22:1000,%22analyticsTags%22:[%22platform:frontend%22,%22type:products%22,%22page:plp%22,%22lang:FR%22,%22country:zh%22]%7D']
    start_urls = cn_urls

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield Request(url, headers=Headers(random.choice(self.headers_list)), dont_filter=True)

    def parse(self, response):
        success = response.status == 200
        if success:
            prod1 = spackage.prodFrToCn()
            data = json.loads(response.body.decode())
            prodList = []
            for each in data['hits']:
                try:
                    prod = []
                    prod.append(each['sku'])
                    prod.append(each['title_zh'])
                    prodList.append(prod)
                except Exception as err:
                    pass
            yield Request(url=self.fr_urls, dont_filter=True, callback=self.tran_parse, meta={'date_cn':prodList})
        else:
            return False

    def tran_parse(self, response):

        success = response.status == 200
        if success:

            prod1 = spackage.prodFrToCn()
            dict = spackage.dict()
            data = json.loads(response.body.decode())
            for each in data['hits']:
                prod1['prodSku'] = each['sku']
                prod1['frName'] = each['title_fr']
                prod1['marque'] = '24s'
                prod1['mainsite'] = 'https://www.24s.com'
                prod1['fromWhere'] = 'produitName'
                prod1['category'] = 'chaussures'
                prod1['cnName'] = ' '
                for i in response.meta['date_cn']:
                    if i[0] == each['sku']:
                        prod1['cnName'] = i[1]
                        del i
                piece_cn = re.split(" ", prod1['cnName'])
                piece_fr = re.split(" ", prod1['frName'])
                isComplete = True
                singleWord_cn = []
                for each in piece_cn:
                    each = each.lower()
                    i = re.match("[a-zA-Z]+", each)
                    if not i is None:
                        have = 0
                        for everyone in piece_fr:
                            everyone = everyone.lower()
                            if each == everyone:
                                have = 1
                        if have == 0:
                            # print('复杂')
                            isComplete = False
                            break
                    singleWord_cn.append(re.sub("[A-Za-z0-9\,\。]", "", each))
                strCn = ''
                for each in singleWord_cn:
                    if len(each)>1:
                        strCn = strCn + each


                # print(piece_cn)
                singleWord_fr = []
                for each in piece_fr:
                    each = each.lower()
                    have = 0
                    for everyone in piece_cn:
                        everyone = everyone.lower()
                        if everyone == each:
                            have = 1
                            break
                    if have == 0:
                        singleWord_fr.append(each)
                # print(piece_fr)
                # print(' '.join(singleWord_fr))
                # print('**********************')

                if isComplete:
                    # print('常规翻译', strCn)
                    dict['wordCn'] = strCn
                    dict['wordFr'] = ' '.join(singleWord_fr)

                if prod1['frName'] == prod1['cnName']:
                    prod1['whetherTrans'] = 'False'
                else:
                    prod1['whetherTrans'] = 'True'
                try:
                    if len(dict['wordCn'])>0 and len(dict['wordFr'])>0:
                        yield dict
                except Exception as err:
                    pass
        else:
            return False



    headers_list = [
        # Chrome
        {
            'authority': 'www.marionnaud.fr',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'referer':'https://www.24s.com/fr-fr/femme/chaussures',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en,fr;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        },
        # IE
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            'referer': 'https://www.24s.com/fr-fr/femme/chaussures',
            "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.7,en;q=0.5,zh-Hans-CN;q=0.3,zh-Hans;q=0.2",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
        },
        # Firefox
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'referer': 'https://www.24s.com/fr-fr/femme/chaussures',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }
    ]