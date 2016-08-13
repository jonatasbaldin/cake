import json
import re

# Import nice CrawlSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Import our Items
from cake_scrap.items import CakeScrapItem


class cake(CrawlSpider):
    """ Crawl posts on TechCrunch and yields information about the articles
        and its author.
    """
    name = 'cake'
    # Wont leave TechCrunch
    allowed_domains = ['techcrunch.com']
    start_urls = [
        'https://techcrunch.com/'
    ]

    # How it will crawl?
    rules = [
        # Extract URLs that have a 'date pattern', like /yyyy/mm/dd/
        Rule(LinkExtractor(
            allow=['/\d*/\d*/\d*/.*/$']),
            callback='parse_item',
            follow=False),
        # Extract all the next pages
        Rule(LinkExtractor(
            allow=['/page/\d*']),
            follow=True)
    ]

    def sanitize_output(self, text):
        """ Removes HTML tags, \n, and \xa0 from string
        """
        html_re = re.compile(r'<[^>]+>')
        return html_re.sub('', text).strip().replace('\n', '').replace('\xa0', '')

    def parse_item(self, response):
        """ Parse the information from TechCrunch
        """
        item = CakeScrapItem()

        # Empty string if author has no Twitter
        try:
            # Extracting with CSS
            item['author_twitter_page'] = response.css('[class="twitter-handle"] a::attr(href)').extract()[0]
        except:
            item['author_twitter_page'] = ''

        # Create full author profile page
        authors_profile_page = response.css('[class="byline"] a::attr(href)').extract()[0]
        item['author_profile_page'] = response.urljoin(authors_profile_page)

        # Get content from ld+json, nice to extract infomation
        content = json.loads(response.css('script[type="application/ld+json"]::text').extract()[1])
        item['article_content'] = self.sanitize_output(content['articleBody'])
        item['article_title'] = content['headline']
        item['article_thumbnail_url'] = content['image']['@list']
        item['author_name'] = content['author']['name']

        item['article_url'] = response.url

        # Extracting with xpath
        item['article_published_date'] = response.xpath('/html/head/meta[@name=\'sailthru.date\']/@content').extract()[0]

        yield item
