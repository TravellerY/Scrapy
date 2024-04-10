# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join
from scrapy.loader import ItemLoader


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def creat_date_conver(value):
    creat_date = re.findall(',*?(\d+.*)', value)
    if creat_date:
        return creat_date
    else:
        return "1970-07-01"


class ArticlecnblogsspiderItem(scrapy.Item):
    title = scrapy.Field()
    created_date = scrapy.Field(
        input_processor=MapCompose(creat_date_conver)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=Identity()
    )
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    content = scrapy.Field()
