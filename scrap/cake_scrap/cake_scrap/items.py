# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CakeScrapItem(scrapy.Item):
    author_name = scrapy.Field()
    author_profile_page = scrapy.Field()
    author_twitter_page = scrapy.Field()
    article_title = scrapy.Field()
    article_content = scrapy.Field()
    article_url = scrapy.Field()
    article_published_date = scrapy.Field()
    article_thumbnail_url = scrapy.Field()
