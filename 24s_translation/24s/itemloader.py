from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars
#不要修改


#这些方法为统一的数据清理方法
def lowercase_processor(values):
    return values.lower()


def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result


def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'')
    result = replace_escape_chars(result, which_ones='EUR', replace_by=u'')
    result = replace_escape_chars(result, which_ones=',', replace_by=u'')

    return result

def clear_line_feed(values):
    result = replace_escape_chars(values, which_ones='\r\n', replace_by=u'')
    result = replace_escape_chars(result, which_ones='\n', replace_by=u'')
    result = replace_escape_chars(result, which_ones='\r', replace_by=u'')
    result = replace_escape_chars(result, which_ones='\t', replace_by=u'')
    return result

def strip(values):
    return values.strip()


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())

#RootTaskSpider
class RootCategoryItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    catalogname_in = MapCompose(remove_tags, clear_line_feed, strip)


class SpiderInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    url = MapCompose(remove_tags, clear_line_feed, strip)

#GetTreeProductList
class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    productUrl_in = MapCompose(remove_tags, processDesc, strip)
    productName_in = MapCompose(remove_tags, processDesc, strip, processDataPrice)
    # imageUrls_in = MapCompose(remove_tags, processDesc, strip)

#ProductTaskSpider
class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    FullDescription_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)


class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    FullDescription_in = MapCompose(remove_tags, processDesc)